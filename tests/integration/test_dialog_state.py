"""Çok-turlu diyalog-durumu (dialog-state) regresyonu.

İLKE: durum yalnız session.user_id verildiğinde aktiftir; sunulmuş bir netleştirme/
bağlamı ÇÖZER, asla uydurmaz. user_id yoksa motor stateless kalır (paylaşılan motorda
kullanıcılar arası sızıntı olmaz) — bu da ayrıca test edilir.
"""

import unittest

from src.engine import Engine


def _run_turns(turns, role, user_id="u1"):
    """Benchmark gibi: case başına yeni engine, aynı user_id ile sıralı turlar."""
    engine = Engine()
    last = None
    for q in turns:
        last = engine.handle({
            "query": q,
            "session": {"role": role, "authenticated": role != "ziyaretci",
                        "user_id": user_id},
        })
    return last


class DialogFollowupTests(unittest.TestCase):
    def test_bare_name_after_report_topic_parent(self) -> None:
        # veli: "çocuğumun karnesi" -> isim -> report_card_view (nav öğrenciye özel: yok)
        r = _run_turns(["Çocuğumun karnesini görmek istiyorum.", "Ahmet."], "veli")
        self.assertEqual(r["intent"], "report_card_view")
        self.assertIsNone(r["navigation"])

    def test_name_and_course_after_report_topic_teacher(self) -> None:
        # öğretmen: karne bağlamı + öğrenci adı+ders -> student_marks_lookup
        r = _run_turns(["Karnemi nerede görürüm?", "Ali, Matematik dersi."], "ogretmen")
        self.assertEqual(r["intent"], "student_marks_lookup")

    def test_ordinal_after_clarify(self) -> None:
        # netleştirme sonrası "Evet, ilki." -> ilk aday (guide_info); clarify DEĞİL
        r = _run_turns(["Bir yerde hata verdi yardım et.", "Evet, ilki."], "ogrenci")
        self.assertNotEqual(r["response_id"], "clarification_prompt")
        self.assertNotIn("tam anlayamadım", r["text"])

    def test_complaint_after_nav(self) -> None:
        # rehber/nav sonrası "Orada yok." -> navigation yardımı
        r = _run_turns(["Rehber sayfası nerede?", "Orada yok."], "ogrenci")
        self.assertIn(r["intent"], ("navigation_help", "access_denied_help"))

    def test_continuation_repeats_last_intent(self) -> None:
        # "Peki sonra?" -> önceki intent'i sürdür (exam_enter_room)
        r = _run_turns(["Sınava nasıl girerim?", "Peki sonra?"], "ogrenci")
        self.assertEqual(r["intent"], "exam_enter_room")


class DialogIsolationTests(unittest.TestCase):
    def test_no_user_id_is_stateless(self) -> None:
        # user_id YOKSA durum tutulmaz: "Peki sonra?" tek başına takip etmez -> clarify/OOS.
        engine = Engine()
        engine.handle({"query": "Sınava nasıl girerim?",
                       "session": {"role": "ogrenci", "authenticated": True}})
        r = engine.handle({"query": "Peki sonra?",
                           "session": {"role": "ogrenci", "authenticated": True}})
        self.assertNotEqual(r["intent"], "exam_enter_room")

    def test_distinct_users_do_not_bleed(self) -> None:
        # Farklı user_id'ler birbirinin bağlamını görmez.
        engine = Engine()
        engine.handle({"query": "Sınava nasıl girerim?",
                       "session": {"role": "ogrenci", "authenticated": True, "user_id": "A"}})
        r = engine.handle({"query": "Peki sonra?",
                           "session": {"role": "ogrenci", "authenticated": True, "user_id": "B"}})
        self.assertNotEqual(r["intent"], "exam_enter_room")


if __name__ == "__main__":
    unittest.main()
