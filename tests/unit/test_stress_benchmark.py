"""10K sözleşme-farkında sentetik/metamorfik stres benchmarkı testleri."""

import json
import re
import tempfile
import unittest
from collections import Counter, defaultdict
from pathlib import Path
from unittest.mock import patch

from src.catalog import INTENTS, ROLE_HIERARCHY
from src.role_spaces import get_role_space
from stress_benchmark import (
    DEFAULT_IN_SCOPE_COUNT,
    DEFAULT_OOS_COUNT,
    DEFAULT_TOTAL_COUNT,
    GENERATOR_VERSION,
    MUTATION_FAMILIES,
    SOCIAL_INTENTS,
    STATE_ERROR_ELIGIBLE,
    collect_results,
    generate_stress_records,
    load_source_seeds,
    main,
    normalise_question_key,
    privacy_findings,
    render_markdown,
    render_markdown_part,
    write_jsonl,
    write_report,
)


def _response(
    *,
    intent: str | None,
    response_id: str,
    outcome: str,
    reason_code: str,
    fallback: bool = False,
    auth_action: str | None = None,
    route: str | None = None,
    route_key: str | None = None,
    text: str = "Kullanıcıya görünen sahte cevap",
) -> dict:
    return {
        "trace_id": "fake",
        "intent": intent,
        "response_id": response_id,
        "text": text,
        "fallback": fallback,
        "auth_action": auth_action,
        "navigation": (
            {"route": route, "label": "Sahte", "available": True}
            if route else None
        ),
        "assistant_meta": {
            "outcome": outcome,
            "action_id": intent,
            "reason_code": reason_code,
            "navigation": {"route_key": route_key} if route_key else None,
        },
        "nested": {"machine_only": [1, 2, 3]},
    }


class _FakeEngine:
    def handle(self, payload: dict) -> dict:
        if payload["query"] == "good":
            result = _response(
                intent="profile_view",
                response_id="profile_view_response",
                outcome="allow",
                reason_code="allowed",
                route="/profile/me",
                route_key="profile",
            )
        elif payload["query"] == "scope":
            result = _response(
                intent=None,
                response_id="out_of_scope_action",
                outcome="deny",
                reason_code="scope_boundary_action",
            )
        elif payload["query"] in {"clarify", "clarify-boundary"}:
            result = _response(
                intent=None,
                response_id="clarification_prompt",
                outcome="clarify",
                reason_code="ambiguous_query",
            )
        else:
            result = _response(
                intent="wrong_intent",
                response_id="wrong_response",
                outcome="allow",
                reason_code="allowed",
                route="/wrong",
                route_key="wrong",
            )
        result["trace_id"] = payload["trace_id"]
        return result


def _fake_record(
    question: str,
    *,
    record_id: str,
    expected: dict,
    family: str = "semantic_paraphrase",
    scope: str = "in_scope",
    scope_boundary_type: str | None = None,
) -> dict:
    expected_intent = expected["intent"] or "oos"
    return {
        "id": record_id,
        "question": question,
        "expected_intent": expected_intent,
        "expected": expected,
        "role": "ogrenci",
        "scope": scope,
        "scope_boundary_type": scope_boundary_type,
        "family": family,
        "transformations": [family],
        "mutation": {"fixture": True, "variant_hash": "0000000000000001"},
        "policy": {
            "outcome": expected["outcome"],
            "action_id": expected["intent"],
            "scope": None,
            "reason_code": expected.get("reason_code"),
            "route_key": expected.get("meta_route_key"),
        },
        "source": {
            "dataset": "fixture",
            "index": 1,
            "question": "seed",
            "role": "ogrenci",
        },
        "synthetic": True,
        "is_gold": False,
        "generator_version": GENERATOR_VERSION,
        "generation_round": 0,
        "privacy_scan": {"passed": True, "findings": []},
    }


ALLOW_EXPECTED = {
    "intent": "profile_view",
    "outcome": "allow",
    "meta_outcome": "allow",
    "meta_action_id": "profile_view",
    "response_ids": ["profile_view_response"],
    "auth_action": None,
    "fallback": False,
    "navigation_route": "/profile/me",
    "meta_route_key": "profile",
    "reason_code": "allowed",
}

FALLBACK_EXPECTED = {
    "intent": None,
    "outcome": "fallback",
    "meta_outcome": "fallback",
    "meta_action_id": None,
    "response_ids": ["fallback_message"],
    "auth_action": None,
    "fallback": True,
    "navigation_route": None,
    "meta_route_key": None,
    "reason_code": "out_of_scope",
}

SCOPE_EXPECTED = {
    "intent": None,
    "outcome": "deny",
    "meta_outcome": "deny",
    "meta_action_id": None,
    "response_ids": ["out_of_scope_action"],
    "auth_action": None,
    "fallback": False,
    "navigation_route": None,
    "meta_route_key": None,
    "reason_code": "scope_boundary_action",
}

DATA_SCOPE_EXPECTED = {
    **SCOPE_EXPECTED,
    "reason_code": "scope_boundary_data",
}


class StressGenerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.records = generate_stress_records()

    def test_exactly_ten_thousand_with_ninety_ten_split(self) -> None:
        self.assertEqual(len(self.records), DEFAULT_TOTAL_COUNT)
        counts = Counter(record["scope"] for record in self.records)
        self.assertEqual(counts, {
            "in_scope": DEFAULT_IN_SCOPE_COUNT,
            "oos": DEFAULT_OOS_COUNT,
        })

    def test_in_scope_is_intent_balanced_and_covers_catalog(self) -> None:
        counts = Counter(
            record["expected_intent"]
            for record in self.records
            if record["scope"] == "in_scope"
        )
        self.assertEqual(set(counts), {item["intent"] for item in INTENTS})
        self.assertLessEqual(max(counts.values()) - min(counts.values()), 1)

    def test_only_human_labeled_sources_are_used_and_catalog_is_never_a_seed(self) -> None:
        sources = {record["source"]["dataset"] for record in self.records}
        self.assertEqual(sources, {"benchmark", "near_oos"})
        self.assertTrue(all(
            record["source"]["dataset"] == "benchmark"
            for record in self.records
            if record["scope"] == "in_scope"
        ))

    def test_all_normalized_questions_and_stable_ids_are_unique(self) -> None:
        keys = [normalise_question_key(record["question"]) for record in self.records]
        ids = [record["id"] for record in self.records]
        self.assertEqual(len(set(keys)), DEFAULT_TOTAL_COUNT)
        self.assertEqual(len(set(ids)), DEFAULT_TOTAL_COUNT)
        self.assertTrue(all(re.fullmatch(r"stress-[0-9a-f]{20}", value) for value in ids))

    def test_smaller_generation_is_deterministic_including_hash_ids(self) -> None:
        kwargs = {"in_scope_count": 176, "oos_count": 64}
        self.assertEqual(generate_stress_records(**kwargs), generate_stress_records(**kwargs))

    def test_every_record_has_version_privacy_and_full_expected_contract(self) -> None:
        required = {
            "intent", "outcome", "meta_outcome", "meta_action_id", "response_ids", "auth_action",
            "fallback", "navigation_route", "meta_route_key", "reason_code",
        }
        for record in self.records:
            self.assertEqual(record["generator_version"], GENERATOR_VERSION)
            self.assertEqual(record["privacy_scan"], {"passed": True, "findings": []})
            self.assertEqual(set(record["expected"]), required)
            self.assertTrue(record["expected"]["response_ids"])

    def test_named_other_person_data_uses_safety_precedence_contract(self) -> None:
        safety_rows = [
            row for row in self.records
            if row["expected_intent"] == "exam_grade_student"
            and row["expected"]["response_ids"] == ["safety_other_person_data"]
        ]
        self.assertTrue(safety_rows)
        for row in safety_rows:
            self.assertIn(row["role"], {"ziyaretci", "veli", "ogrenci"})
            self.assertIsNone(row["expected"]["intent"])
            self.assertEqual(row["expected"]["outcome"], "deny")
            self.assertEqual(row["expected"]["reason_code"], "safety_other_person_data")

    def test_policy_metadata_comes_from_real_role_space_matrix(self) -> None:
        generated_outcomes: dict[str, set[str]] = defaultdict(set)
        for record in self.records:
            if record["scope"] != "in_scope":
                continue
            intent = record["expected_intent"]
            view = get_role_space(record["role"]).view_for(intent)
            self.assertIsNotNone(view)
            if record["expected"]["response_ids"] == ["safety_other_person_data"]:
                # Safety, intent rol matrisinden önce çalışan ayrı bir kapıdır.
                generated_outcomes[intent].add(view.outcome.value)
                continue
            redirect_targets = {
                "report_card_view": "student_marks_lookup",
                "attendance_view": "student_attendance_lookup",
                "exam_finish_result": "student_marks_lookup",
            }
            if record["role"] in {"ogretmen", "yonetici", "admin"} and intent in redirect_targets:
                view = get_role_space(record["role"]).view_for(redirect_targets[intent])
            self.assertEqual(record["policy"]["outcome"], view.outcome.value)
            self.assertEqual(record["policy"]["action_id"], view.action_id)
            self.assertEqual(record["policy"]["route_key"], view.route_key)
            generated_outcomes[intent].add(view.outcome.value)

        for item in INTENTS:
            intent = item["intent"]
            matrix_outcomes = {
                get_role_space(role).view_for(intent).outcome.value
                for role in ROLE_HIERARCHY
            }
            self.assertTrue(matrix_outcomes.issubset(generated_outcomes[intent]))

    def test_denied_cases_expect_correct_auth_action_and_no_routes(self) -> None:
        denied = [
            record for record in self.records
            if record["scope"] == "in_scope"
            and record["policy"]["outcome"] == "deny"
            and record["expected"]["outcome"] == "deny"
        ]
        self.assertTrue(denied)
        for record in denied:
            if record["expected"]["response_ids"] == ["safety_other_person_data"]:
                self.assertIsNone(record["expected"]["auth_action"])
                self.assertIsNone(record["expected"]["navigation_route"])
                self.assertIsNone(record["expected"]["meta_route_key"])
                continue
            expected_auth = (
                "login_required" if record["role"] == "ziyaretci"
                else "role_insufficient"
            )
            self.assertEqual(record["expected"]["auth_action"], expected_auth)
            self.assertIsNone(record["expected"]["navigation_route"])
            self.assertIsNone(record["expected"]["meta_route_key"])

    def test_rich_families_exist_and_invalid_error_frames_do_not(self) -> None:
        self.assertEqual(
            {record["family"] for record in self.records},
            set(MUTATION_FAMILIES),
        )
        for record in self.records:
            if record["expected_intent"] not in STATE_ERROR_ELIGIBLE:
                self.assertNotIn("state_error", record["transformations"])
            if record["scope"] == "oos":
                self.assertNotIn("state_error", record["transformations"])

    def test_punctuation_and_case_do_not_fake_question_uniqueness(self) -> None:
        self.assertEqual(
            normalise_question_key("  Sınava nasıl girerim?!  "),
            normalise_question_key("sınava NASIL girerim..."),
        )

    def test_nav_overview_accepts_dynamic_section_response(self) -> None:
        nav_rows = [
            row for row in self.records
            if row["scope"] == "in_scope" and row["expected_intent"] == "nav_overview"
        ]
        self.assertTrue(nav_rows)
        self.assertTrue(all(
            "section_overview" in row["expected"]["response_ids"]
            for row in nav_rows
        ))

    def test_upper_role_report_redirect_uses_served_target_contract(self) -> None:
        rows = [
            row for row in self.records
            if row["expected_intent"] == "exam_finish_result"
            and row["role"] in {"ogretmen", "yonetici", "admin"}
        ]
        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row["expected"]["outcome"], "allow")
            self.assertEqual(row["expected"]["response_ids"], ["student_report_redirect"])
            self.assertEqual(row["expected"]["meta_action_id"], "student_marks_lookup")
            self.assertEqual(row["expected"]["meta_route_key"], "student_marks")
            self.assertEqual(row["expected"]["reason_code"], "allowed")
            self.assertEqual(row["policy"]["outcome"], "allow")

    def test_ascii_typo_semantic_ui_and_hash_variant_contracts(self) -> None:
        ascii_rows = [r for r in self.records if r["family"] == "turkish_ascii"]
        typo_rows = [r for r in self.records if r["family"] == "single_typo"]
        semantic_rows = [r for r in self.records if r["family"] == "semantic_paraphrase"]
        ui_rows = [r for r in self.records if r["family"] == "ui_label_tr_en"]
        self.assertTrue(all(row["question"].isascii() for row in ascii_rows))
        self.assertTrue(all(row["mutation"]["typo_count"] == 1 for row in typo_rows))
        self.assertTrue(all(
            row["mutation"]["strategy"] in {
                "lexical_replacement", "meaning_preserving_frame",
            }
            for row in semantic_rows if row["scope"] == "in_scope"
        ))
        self.assertTrue(all(
            row["mutation"]["strategy"] == "neutral_scope_frame"
            for row in semantic_rows if row["scope"] == "oos"
        ))
        self.assertTrue(ui_rows)
        self.assertTrue(all(row["mutation"]["strategy"] in {
            "inline_label", "screen_context",
        } for row in ui_rows))
        self.assertGreater(
            len({row["mutation"]["variant_hash"] for row in self.records}),
            len(self.records) // 2,
        )

    def test_mutations_preserve_natural_language_and_intent_semantics(self) -> None:
        lowered = [row["question"].casefold() for row in self.records]
        invalid_fragments = (
            "eklemek yapmam gerekiyor", "değiştirmek yapmam gerekiyor",
            "silmek yapmam gerekiyor", "yeni kayıt girmek",
            "yeni kayıt açmak", "üyeliğini sonlandırmak",
        )
        for fragment in invalid_fragments:
            self.assertFalse(any(fragment in question for question in lowered), fragment)

        social_semantic = [
            row["question"].casefold() for row in self.records
            if row["scope"] == "in_scope"
            and row["expected_intent"] in SOCIAL_INTENTS
            and row["family"] == "semantic_paraphrase"
        ]
        self.assertTrue(social_semantic)
        self.assertTrue(all("işlem yolunu" not in question for question in social_semantic))

        board_view_states = [
            row["question"].casefold() for row in self.records
            if row["expected_intent"] == "board_view" and row["family"] == "state_error"
        ]
        self.assertTrue(board_view_states)
        self.assertTrue(all("yeniden açamıyorum" not in question for question in board_view_states))

    def test_oos_mutations_use_neutral_language_and_keep_boundary_semantics(self) -> None:
        oos = [record for record in self.records if record["scope"] == "oos"]
        self.assertTrue(oos)
        product_frame_fragments = (
            "hezarfen'de", "hezarfende", "uygulamada", "hangi ekran",
            "hangi ekrandan", "hangi ekranda", "hangi adım", "hangi adim",
            "işlem akışı", "islem akisi", "doğru ekran", "dogru ekran",
            "nereden başlamalı", "nereden baslamali", "panelinden",
            "hesabımla", "hesabimla", "hangi sayfaya",
        )
        for row in oos:
            folded = row["question"].casefold()
            self.assertFalse(
                any(fragment in folded for fragment in product_frame_fragments),
                msg=f"ürün-içi OOS çerçevesi: {row['question']}",
            )
            expected_semantics = row["scope_boundary_type"] or "fallback"
            self.assertEqual(row["mutation"]["scope_framing"], "neutral_oos")
            self.assertEqual(row["mutation"]["boundary_semantics"], expected_semantics)

        action_rows = [row for row in oos if row["scope_boundary_type"] == "action"]
        self.assertTrue(action_rows)
        self.assertTrue(all(row["expected"]["outcome"] == "deny" for row in action_rows))

    def test_oos_fallback_and_scope_boundary_metadata_are_separate(self) -> None:
        oos = [record for record in self.records if record["scope"] == "oos"]
        boundary = [record for record in oos if record["scope_boundary_type"]]
        fallback = [record for record in oos if not record["scope_boundary_type"]]
        self.assertTrue(boundary)
        self.assertTrue(fallback)
        self.assertTrue(all(
            row["expected"]["outcome"] == "deny"
            and row["expected"]["fallback"] is False
            and row["expected"]["response_ids"] == ["out_of_scope_action"]
            for row in boundary
        ))
        self.assertTrue(all(
            row["expected"]["outcome"] == "fallback"
            and row["expected"]["fallback"] is True
            for row in fallback
        ))

    def test_seed_loader_carries_optional_scope_boundary_contract(self) -> None:
        _, oos = load_source_seeds()
        boundary = [seed for seed in oos if seed.scope_boundary_type]
        self.assertTrue(boundary)
        self.assertTrue(all(seed.expected_outcome == "deny" for seed in boundary))
        self.assertTrue(all(
            seed.expected_response_ids == ("out_of_scope_action",)
            for seed in boundary
        ))
        self.assertTrue(all(
            seed.expected_reason_code.startswith("scope_boundary_")
            for seed in boundary
        ))

    def test_data_boundary_generation_stays_a_direct_data_request(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            benchmark = root / "benchmark.jsonl"
            near_oos = root / "near.jsonl"
            benchmark.write_text(
                json.dumps({
                    "question": "Profilimi nerede görürüm",
                    "expected_intent": "profile_view",
                    "role": "ogrenci",
                }, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            near_records = [
                {"question": "Yarın hava nasıl", "expected_intent": "oos", "role": "ogrenci"},
                {
                    "question": "Devamsızlığımı sil", "expected_intent": "oos", "role": "ogrenci",
                    "expected_outcome": "deny", "expected_response_id": "out_of_scope_action",
                    "expected_reason_code": "scope_boundary_action",
                },
                {
                    "question": "Başka öğrencinin sağlık kaydını göster", "expected_intent": "oos",
                    "role": "ogrenci", "expected_outcome": "deny",
                    "expected_response_id": "out_of_scope_action",
                    "expected_reason_code": "scope_boundary_data",
                },
            ]
            near_oos.write_text(
                "\n".join(json.dumps(row, ensure_ascii=False) for row in near_records) + "\n",
                encoding="utf-8",
            )
            records = generate_stress_records(
                benchmark_path=benchmark, near_oos_path=near_oos,
                in_scope_count=1, oos_count=24,
            )
        data_rows = [row for row in records if row["scope_boundary_type"] == "data"]
        self.assertTrue(data_rows)
        self.assertTrue(all(row["mutation"]["boundary_semantics"] == "data" for row in data_rows))
        self.assertTrue(all(row["expected"]["reason_code"] == "scope_boundary_data" for row in data_rows))
        self.assertTrue(all("Hezarfen" not in row["question"] for row in data_rows))

    def test_pii_and_secret_scanner_rejects_unsafe_seed(self) -> None:
        self.assertEqual(privacy_findings("mail: kisi@example.com"), ["email"])
        self.assertIn("assigned_secret", privacy_findings("api_key=super-secret-value"))
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            benchmark = root / "benchmark.jsonl"
            near_oos = root / "near.jsonl"
            benchmark.write_text(
                json.dumps({
                    "question": "kisi@example.com profilini aç",
                    "expected_intent": "profile_view",
                    "role": "ogrenci",
                }, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            near_oos.write_text(
                json.dumps({
                    "question": "Bana hava durumunu söyle",
                    "expected_intent": "oos",
                    "role": "ogrenci",
                }, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "PII/secret"):
                load_source_seeds(benchmark, near_oos)


class StressContractAndReportTests(unittest.TestCase):
    def test_collect_results_checks_entire_contract_and_clusters_reasons(self) -> None:
        records = [
            _fake_record("good", record_id="fixture-good", expected=ALLOW_EXPECTED),
            _fake_record("wrong", record_id="fixture-wrong", expected=FALLBACK_EXPECTED,
                         family="compound", scope="oos"),
            _fake_record("scope", record_id="fixture-scope", expected=SCOPE_EXPECTED,
                         family="sentence_form", scope="oos"),
        ]
        rows = collect_results(records, engine=_FakeEngine())
        self.assertTrue(rows[0]["passed"])
        self.assertFalse(rows[1]["passed"])
        self.assertTrue(rows[2]["passed"])
        self.assertEqual(rows[0]["response"]["trace_id"], "stress-00001")
        self.assertIn("intent_mismatch", rows[1]["failure_reasons"])
        self.assertIn("outcome_mismatch", rows[1]["failure_reasons"])
        self.assertIn("response_id_mismatch", rows[1]["failure_reasons"])
        self.assertIn("fallback_mismatch", rows[1]["failure_reasons"])
        self.assertIn("navigation_route_mismatch", rows[1]["failure_reasons"])
        self.assertIn("meta_route_key_mismatch", rows[1]["failure_reasons"])
        self.assertEqual(rows[1]["failure_severity"], "hard")

    def test_only_safe_oos_fallback_clarification_is_soft_and_remains_failed(self) -> None:
        rows = collect_results([
            _fake_record(
                "clarify", record_id="fixture-soft", expected=FALLBACK_EXPECTED,
                scope="oos",
            ),
            _fake_record(
                "clarify-boundary", record_id="fixture-boundary-hard",
                expected=SCOPE_EXPECTED, scope="oos", scope_boundary_type="action",
            ),
        ], engine=_FakeEngine())
        self.assertFalse(rows[0]["passed"])
        self.assertEqual(rows[0]["failure_severity"], "soft")
        self.assertIn("fallback_mismatch", rows[0]["failure_reasons"])
        self.assertFalse(rows[1]["passed"])
        self.assertEqual(rows[1]["failure_severity"], "hard")

    def test_summary_has_required_breakdowns_without_full_engine_json(self) -> None:
        rows = collect_results([
            _fake_record("wrong", record_id="fixture-in-scope-fail", expected=ALLOW_EXPECTED),
            _fake_record("wrong", record_id="fixture-wrong", expected=FALLBACK_EXPECTED,
                         family="compound", scope="oos"),
            _fake_record("clarify", record_id="fixture-soft", expected=FALLBACK_EXPECTED,
                         scope="oos"),
            _fake_record("wrong", record_id="fixture-action", expected=SCOPE_EXPECTED,
                         scope="oos", scope_boundary_type="action"),
            _fake_record("wrong", record_id="fixture-data", expected=DATA_SCOPE_EXPECTED,
                         scope="oos", scope_boundary_type="data"),
        ], engine=_FakeEngine())
        markdown = render_markdown(rows, part_links=["parts/part-0001.md"])
        self.assertIn("gold benchmark değildir", markdown)
        self.assertIn("Kaynak bazında", markdown)
        self.assertIn("Beklenen outcome bazında", markdown)
        self.assertIn("Gerçek outcome bazında", markdown)
        self.assertIn("Hata kümeleri", markdown)
        self.assertIn("intent_mismatch", markdown)
        self.assertIn("OOS türü ve FAIL şiddeti", markdown)
        self.assertRegex(markdown, r"\| `fallback` \| 2 \| 0 \| 1 \| 1 \|")
        self.assertRegex(markdown, r"\| `action-boundary` \| 1 \| 0 \| 0 \| 1 \|")
        self.assertRegex(markdown, r"\| `data-boundary` \| 1 \| 0 \| 0 \| 1 \|")
        self.assertIn("İlk uygulama-içi FAIL örnekleri", markdown)
        self.assertIn("fixture-in-scope-fail", markdown)
        self.assertIn("İlk OOS FAIL örnekleri", markdown)
        self.assertIn("fixture-soft", markdown)
        self.assertIn("parts/part-0001.md", markdown)
        self.assertNotIn('"machine_only": [', markdown)

    def test_markdown_part_contains_visible_text_not_machine_payload(self) -> None:
        rows = collect_results([
            _fake_record("good", record_id="fixture-good", expected=ALLOW_EXPECTED),
        ], engine=_FakeEngine())
        part = render_markdown_part(rows, part_number=1, total_parts=1)
        self.assertIn("Kullanıcıya görünen sahte cevap", part)
        self.assertIn("### Soru", part)
        self.assertIn("kısa inceleme metadata'sı", part)
        self.assertNotIn("yalnız kullanıcıya görünen metin", part)
        self.assertNotIn("machine_only", part)

    def test_oos_report_exposes_zero_coverage_boundary_classes(self) -> None:
        rows = collect_results([
            _fake_record("good", record_id="fixture-good", expected=ALLOW_EXPECTED),
        ], engine=_FakeEngine())
        markdown = render_markdown(rows)
        self.assertIn("| `fallback` | 0 | 0 | 0 | 0 | 0.0% |", markdown)
        self.assertIn("| `action-boundary` | 0 | 0 | 0 | 0 | 0.0% |", markdown)
        self.assertIn("| `data-boundary` | 0 | 0 | 0 | 0 | 0.0% |", markdown)

    def test_report_writer_creates_250_case_parts_and_jsonl_keeps_full_response(self) -> None:
        base_row = collect_results([
            _fake_record("good", record_id="fixture-good", expected=ALLOW_EXPECTED),
        ], engine=_FakeEngine())[0]
        rows = []
        for index in range(1, 502):
            row = dict(base_row)
            row["index"] = index
            row["id"] = f"fixture-{index:04d}"
            rows.append(row)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            custom_results = root / "results-special.jsonl"
            report = write_report(
                rows, root / "summary.md", chunk_size=250,
                results_path=custom_results,
            )
            parts = sorted((root / "summary_parcalar").glob("part-*.md"))
            self.assertEqual(len(parts), 3)
            self.assertIn("part-0003.md", report.read_text(encoding="utf-8"))
            self.assertIn("results-special.jsonl", report.read_text(encoding="utf-8"))

            part_dir = root / "summary_parcalar"
            (part_dir / "part-9999.md").write_text("stale generated", encoding="utf-8")
            (part_dir / "inceleme-notlari.md").write_text("koru", encoding="utf-8")
            sibling = root / "baska_rapor_parcalar"
            sibling.mkdir()
            sibling_part = sibling / "part-0001.md"
            sibling_part.write_text("koru", encoding="utf-8")
            write_report(
                rows[:251], root / "summary.md", chunk_size=250,
                results_path=custom_results,
            )
            remaining_parts = sorted(path.name for path in part_dir.glob("part-*.md") if path.is_file())
            self.assertEqual(remaining_parts, ["part-0001.md", "part-0002.md"])
            self.assertEqual((part_dir / "inceleme-notlari.md").read_text(encoding="utf-8"), "koru")
            self.assertEqual(sibling_part.read_text(encoding="utf-8"), "koru")

            result_path = write_jsonl(rows, root / "results.jsonl")
            persisted = json.loads(result_path.read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(persisted["response"]["nested"]["machine_only"], [1, 2, 3])

    def test_report_chunk_size_is_limited_to_reviewable_range(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, "250-500"):
                write_report([], Path(temporary) / "summary.md", chunk_size=249)
            with self.assertRaisesRegex(ValueError, "250-500"):
                write_report([], Path(temporary) / "summary.md", chunk_size=501)

    def test_cli_is_diagnostic_by_default_and_strict_only_on_request(self) -> None:
        failed_rows = [{"passed": False}]
        fake_return = (Path("data.jsonl"), Path("summary.md"), failed_rows)
        with patch("stress_benchmark.build_artifacts", return_value=fake_return):
            self.assertEqual(main([]), 0)
            self.assertEqual(main(["--allow-failures"]), 0)
            self.assertEqual(main(["--strict"]), 1)


if __name__ == "__main__":
    unittest.main()
