"""Mutasyon testi — kritik invariant'ların test/probe gücünü ölçer.

Fikir (CheckList/mutation testing): kuralları KASITLI boz, kritik invariant
probe'larının bunu YAKALADIĞINI doğrula. Yakalanan mutasyon = "öldürülen".
    mutation_score = öldürülen / toplam
Kritik invariant'lar için hedef %100'dür: yani gizlilik/collision/rol koruması
sağlayan hiçbir kural, testler fark etmeden bozulamamalı.

Bu harness kural KATALOĞUNU (`rules._RAW_RULES`) bellek içinde mutasyona uğratır,
yeniden derler, `get_role_space` önbelleğini temizler, probe'ları koşar ve GERİ ALIR.
Kaynak dosyaya DOKUNMAZ. Çalıştırma: ``python -m src.evaluation.mutation``.
"""

from __future__ import annotations

import copy
from typing import Any, Callable

from .. import rules as rules_mod
from ..engine import Engine
from ..role_spaces import get_role_space


# --- Kritik invariant probe'ları -------------------------------------------
# (ad, sorgu, rol, invariant(resp)->bool). invariant, DOĞRU davranışta True döner;
# mutasyon onu bozarsa False (yakalandı).
Probe = tuple[str, str, str, Callable[[dict[str, Any]], bool]]

def _intent_is(name: str) -> Callable[[dict[str, Any]], bool]:
    return lambda r: r.get("intent") == name

def _intent_not(name: str) -> Callable[[dict[str, Any]], bool]:
    return lambda r: r.get("intent") != name

def _safety_cat(cat: str) -> Callable[[dict[str, Any]], bool]:
    return lambda r: (r.get("safety") or {}).get("category") == cat


PROBES: list[Probe] = [
    ("privacy_arkadas", "Sınıf arkadaşımın devamsızlığını söyle", "ogrenci",
     _intent_is("privacy_security")),
    ("privacy_baska_not", "Başka bir öğrencinin notunu görebilir miyim", "ogrenci",
     _intent_is("privacy_security")),
    ("exam_rejoin", "Sınava ikinci kez girme hakkım var mı?", "ogrenci",
     _intent_not("exam_enter_room")),
    ("attendance_policy", "Geç kalma devamsızlığa mı yazılır?", "ogrenci",
     _intent_not("attendance_view")),
    ("marks_own", "Ders notlarım listeleniyor", "ogrenci",
     _intent_is("report_card_view")),  # 'ders notlarım' -> karne (course_view none[not])
]


# --- Mutasyonlar (kural kataloğunu bozar) -----------------------------------
# Her mutasyon deepcopy edilmiş _RAW_RULES'u alır, bozar, döndürür.
Mutation = tuple[str, Callable[[list[dict[str, Any]]], list[dict[str, Any]]]]


def _drop_groups(raw, intent, token):
    """intent'in 'all' listesi token içeren gruplarını siler."""
    for rule in raw:
        if rule["intent"] == intent:
            rule["groups"] = [g for g in rule["groups"] if token not in g.get("all", [])]
    return raw


def _strip_none(raw, intent, token, all_kw=None):
    """intent gruplarından bir 'none' token'ını kaldırır (all_kw verilirse yalnız o grup)."""
    for rule in raw:
        if rule["intent"] == intent:
            for g in rule["groups"]:
                if all_kw is not None and g.get("all") != all_kw:
                    continue
                if token in g.get("none", []):
                    g["none"] = [t for t in g["none"] if t != token]
    return raw


def _strip_all_none(raw, intent, all_kw=None):
    """intent gruplarının TÜM none-guard'ını boşaltır (yük taşıyan korumayı kaldırır).

    all_kw verilirse yalnız o 'all' imzasına sahip grup; aksi halde tüm gruplar."""
    for rule in raw:
        if rule["intent"] == intent:
            for g in rule["groups"]:
                if all_kw is not None and g.get("all") != all_kw:
                    continue
                g["none"] = []
    return raw


MUTATIONS: list[Mutation] = [
    ("privacy: 'arkadaş' tetikleyicisini sil",
     lambda raw: _drop_groups(raw, "privacy_security", "arkadaş")),
    ("privacy: 'arkadaş+devamsız' kombosunu sil",
     lambda raw: [r for r in raw if not (r["intent"] == "privacy_security"
                  and any(g.get("all") == ["arkadaş", "devamsız"] for g in r["groups"]))
                  ] or raw),
    ("student_marks: {öğrenci,not,gör} none-guard'ını boşalt",
     lambda raw: _strip_all_none(raw, "student_marks_lookup", ["öğrenci", "not", "gör"])),
    ("exam_enter: {sınav,gir} none-guard'ını boşalt",
     lambda raw: _strip_all_none(raw, "exam_enter_room", ["sınav", "gir"])),
    ("attendance_view: {devamsız} none-guard'ını boşalt",
     lambda raw: _strip_all_none(raw, "attendance_view", ["devamsız"])),
    ("course_view: 'not' none-guard'ını kaldır (karne çakışması)",
     lambda raw: _strip_none(raw, "course_view", "not")),
]


def _run_probes() -> dict[str, bool]:
    """Her probe için invariant tutuyor mu? (True=doğru davranış)."""
    engine = Engine()
    results: dict[str, bool] = {}
    for name, query, role, invariant in PROBES:
        resp = engine.handle({
            "query": query,
            "session": {"role": role, "authenticated": role != "ziyaretci"},
        })
        results[name] = invariant(resp)
    return results


def _apply(mutate: Callable) -> None:
    raw = copy.deepcopy(rules_mod._RAW_RULES)
    mutated = mutate(raw)
    rules_mod._RULES = rules_mod._compile_rules(mutated)
    get_role_space.cache_clear()


def _restore(original_rules) -> None:
    rules_mod._RULES = original_rules
    get_role_space.cache_clear()


def compute() -> dict[str, Any]:
    original = rules_mod._RULES

    # 0) Temel: mutasyonsuz tüm probe'lar tutmalı (aksi halde harness geçersiz).
    baseline = _run_probes()

    rows: list[dict[str, Any]] = []
    try:
        for name, mutate in MUTATIONS:
            _apply(mutate)
            after = _run_probes()
            _restore(original)
            # Öldürüldü mü? En az bir probe temelde True iken şimdi False olmalı.
            killed = any(baseline[k] and not after[k] for k in after)
            broke = [k for k in after if baseline[k] and not after[k]]
            rows.append({"mutation": name, "killed": killed, "caught_by": broke})
    finally:
        _restore(original)

    killed = sum(1 for r in rows if r["killed"])
    return {
        "baseline_all_hold": all(baseline.values()),
        "baseline": baseline,
        "rows": rows,
        "killed": killed,
        "total": len(rows),
        "score": killed / len(rows) if rows else 0.0,
    }


def format_report(report: dict[str, Any]) -> str:
    lines = [
        "============== MUTASYON TESTİ (kritik invariant) ==============",
        f"Temel probe'lar hepsi tutuyor : {'EVET' if report['baseline_all_hold'] else 'HAYIR (!!)'}",
        f"Mutation score (öldürülen)    : {report['killed']}/{report['total']} "
        f"= {report['score']:.0%}  (kritik hedef %100)",
        "--- Mutasyonlar ---",
    ]
    for r in report["rows"]:
        mark = "KILLED " if r["killed"] else "SURVIVED"  # survived = test açığı!
        by = (", ".join(r["caught_by"])) if r["caught_by"] else "—"
        lines.append(f"  [{mark}] {r['mutation']}  (yakalayan: {by})")
    if report["score"] < 1.0:
        lines.append("")
        lines.append("UYARI: SURVIVED mutasyonlar = testlerin/probe'ların yakalayamadığı "
                     "kritik kural bozulmaları. Probe seti veya kural sağlamlaştırılmalı.")
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_report(compute()))
