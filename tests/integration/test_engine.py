"""Aşama 12 integration testleri: backend motoru + sözleşme."""

import unittest

from src.engine import Engine, RequestError, handle_request


class ContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = Engine()

    def test_response_has_contract_keys(self) -> None:
        resp = self.engine.handle({"query": "Merhaba"})
        for key in [
            "trace_id", "response_id", "text", "intent",
            "confidence", "fallback", "auth_action", "required_role",
            "navigation", "clarification", "answers", "suggestions",
        ]:
            self.assertIn(key, resp)

    def test_help_capabilities_is_role_scoped(self) -> None:
        # Oturum rolü belliyse "neler yapabilirim" o role özel yanıt döner.
        student = self.engine.handle({"query": "neler yapabilirim",
                                      "session": {"role": "ogrenci", "authenticated": True}})
        self.assertEqual(student["intent"], "help_capabilities")
        self.assertIn("Öğrenci olarak", student["text"])
        teacher = self.engine.handle({"query": "neler yapabilirim",
                                      "session": {"role": "ogretmen", "authenticated": True}})
        self.assertIn("Öğretmen olarak", teacher["text"])
        # Ziyaretçi (rol yok) -> jenerik "rolünü söyle" metni.
        visitor = self.engine.handle({"query": "neler yapabilirim"})
        self.assertIn("Rolünü", visitor["text"])

    def test_log_query_is_pii_masked(self) -> None:
        # KVKK: log_sink'e giden trace'te ham sorgu değil, MASKELİ sorgu bulunur.
        captured = []
        engine = Engine(log_sink=captured.append)
        engine.handle({"query": "numaram 05321234567 kaydeder misin",
                       "session": {"role": "ogrenci", "authenticated": True}})
        self.assertTrue(captured)
        logged = captured[-1].get("query_masked", "")
        self.assertNotIn("05321234567", logged)   # ham numara loglanmadı
        self.assertNotIn("raw_query", captured[-1])  # eski ham alan yok

    def test_suggestions_are_role_based(self) -> None:
        resp = self.engine.handle({"query": "merhaba",
                                   "session": {"role": "ogretmen", "authenticated": True}})
        self.assertIn("Sınav nasıl oluşturulur?", resp["suggestions"])
        visitor = self.engine.handle({"query": "merhaba"})
        self.assertIn("Hezarfen nedir?", visitor["suggestions"])

    def test_english_role_names_accepted(self) -> None:
        # Gerçek backend rolleri İngilizce çözer (student/teacher/manager/admin).
        resp = self.engine.handle({"query": "sınav oluşturmak istiyorum",
                                   "session": {"role": "teacher", "authenticated": True}})
        self.assertEqual(resp["intent"], "exam_create")
        self.assertIsNone(resp["auth_action"])
        resp = self.engine.handle({"query": "karnemi görmek istiyorum",
                                   "session": {"role": "student", "authenticated": True}})
        self.assertEqual(resp["intent"], "report_card_view")

    def test_navigation_route_for_intent(self) -> None:
        # Karne sorusu -> /marks sayfasına yönlendirme (rol yeterli -> available).
        resp = self.engine.handle({"query": "karnemi nerede görürüm",
                                   "session": {"role": "ogrenci", "authenticated": True}})
        self.assertIsNotNone(resp["navigation"])
        self.assertEqual(resp["navigation"]["route"], "/marks")
        self.assertTrue(resp["navigation"]["available"])

    def test_navigation_hidden_when_role_insufficient(self) -> None:
        # No-leak: öğrenci sınav oluşturamaz -> ret; rota/route SIZDIRILMAZ (None).
        resp = self.engine.handle({"query": "sınav nasıl oluşturulur",
                                   "session": {"role": "ogrenci", "authenticated": True}})
        self.assertEqual(resp["auth_action"], "role_insufficient")
        self.assertIsNone(resp["navigation"])

    def test_no_navigation_for_info_intent(self) -> None:
        # Selamlama gibi sayfası olmayan intent -> navigation None.
        resp = self.engine.handle({"query": "merhaba"})
        self.assertIsNone(resp["navigation"])

    def test_bare_role_gives_role_capabilities(self) -> None:
        # 'Öğrenci' tek başına -> rol yetenek özeti (yanlışlıkla 'öğrenci kaydet' değil).
        resp = self.engine.handle({"query": "Öğrenci",
                                   "session": {"role": "ogrenci", "authenticated": True}})
        self.assertEqual(resp["response_id"], "role_capabilities_ogrenci")
        self.assertIn("Karnem", resp["text"])
        self.assertFalse(resp["fallback"])

    def test_role_declaration_with_filler(self) -> None:
        resp = self.engine.handle({"query": "ben öğretmenim",
                                   "session": {"role": "ogretmen", "authenticated": True}})
        self.assertEqual(resp["response_id"], "role_capabilities_ogretmen")

    def test_role_word_inside_real_query_is_not_declaration(self) -> None:
        # İçinde rol kelimesi geçen gerçek sorgu -> boru hattına gider, rol beyanı DEĞİL.
        resp = self.engine.handle({"query": "öğrenci notlarını nasıl görürüm",
                                   "session": {"role": "ogretmen", "authenticated": True}})
        self.assertFalse(resp["response_id"].startswith("role_capabilities"))
        self.assertIsNotNone(resp["intent"])


class LowConfidenceAskTests(unittest.TestCase):
    """Belirsiz bölge (benzerlik güveni < 0.30): tam cevap YERİNE kibar netleştirme.

    Kullanıcı bulgusu: 'Rolüm ne benim' 0.183 güvenle oturum-süresi cevabı almıştı.
    Artık bu bölgede 'anlayamadım — bunu mu demek istedin?' + adaylar döner.
    """

    def setUp(self) -> None:
        self.engine = Engine()

    def _ask(self, q: str) -> dict:
        return self.engine.handle({"query": q,
                                   "session": {"role": "ogrenci", "authenticated": True}})

    def test_low_confidence_asks_instead_of_answering(self) -> None:
        resp = self._ask("bir yerde hata verdi yardım et")
        self.assertEqual(resp["response_id"], "clarification_prompt")
        self.assertIsNone(resp["intent"])          # tahmin dayatılmadı
        self.assertFalse(resp["fallback"])         # tam ret de değil: seçenek sunuldu
        self.assertIn("anlayamadım", resp["text"])
        clar = resp["clarification"]
        self.assertIsNotNone(clar)
        self.assertEqual(len(clar["candidates"]), 2)
        self.assertLess(resp["confidence"], 0.30)

    def test_confident_similarity_still_answers(self) -> None:
        # Orta/yüksek güvende davranış değişmedi: cevap + (yakınsa) çipler.
        resp = self._ask("devamsızlığımı nereden takip ederim")
        self.assertEqual(resp["intent"], "attendance_view")
        self.assertNotEqual(resp["response_id"], "clarification_prompt")

    def test_rule_decisions_never_ask(self) -> None:
        resp = self._ask("karnemi görmek istiyorum")
        self.assertEqual(resp["intent"], "report_card_view")
        self.assertEqual(resp["confidence"], 1.0)

    def test_users_original_query_now_answered_by_rule(self) -> None:
        # 'Rolüm ne benim' artık kural katmanında roles_permissions'a bağlanır.
        resp = self._ask("Rolüm ne benim")
        self.assertEqual(resp["intent"], "roles_permissions")
        self.assertIn("hesap kutusunda", resp["text"])


class MultiIntentTests(unittest.TestCase):
    """Tek mesajda 2-3 istek -> HEPSİNE cevap (answers listesi)."""

    def setUp(self) -> None:
        self.engine = Engine()

    def _ask(self, q: str, role: str = "ogretmen") -> dict:
        return self.engine.handle({"query": q,
                                   "session": {"role": role, "authenticated": True}})

    def test_two_requests_both_answered(self) -> None:
        resp = self._ask("sınav oluştur ve yoklama al")
        self.assertIsNotNone(resp["answers"])
        self.assertEqual([a["intent"] for a in resp["answers"]],
                         ["exam_create", "roll_call"])
        # Birleşik metin iki bölümü de içerir; sözleşme ilk cevabı yansıtır.
        self.assertIn("1)", resp["text"])
        self.assertIn("2)", resp["text"])
        self.assertEqual(resp["intent"], "exam_create")

    def test_three_requests_all_answered(self) -> None:
        resp = self._ask("sınav oluştur ve yoklama al ve etkinlik oluştur")
        self.assertEqual([a["intent"] for a in resp["answers"]],
                         ["exam_create", "roll_call", "event_create"])
        self.assertIn("3)", resp["text"])

    def test_each_answer_has_own_navigation_and_auth(self) -> None:
        # Öğrencide her parçanın kendi yetki durumu; ret'te rota SIZDIRILMAZ.
        resp = self._ask("sınav oluştur ve yoklama al", role="ogrenci")
        for ans in resp["answers"]:
            self.assertEqual(ans["auth_action"], "role_insufficient")
            self.assertIsNone(ans["navigation"])

    def test_natural_ve_is_not_split(self) -> None:
        # 'roller ve yetkiler nedir' TEK sorudur; parçalar kurala çarpmaz -> bölünmez.
        resp = self._ask("roller ve yetkiler nedir", role="ogrenci")
        self.assertIsNone(resp["answers"])
        self.assertEqual(resp["intent"], "roles_permissions")

    def test_duplicate_intent_segments_not_multi(self) -> None:
        # İki parça da AYNI intent'e çıkarsa tek cevap yeter.
        resp = self._ask("sınav oluştur ve yeni sınav hazırla")
        self.assertIsNone(resp["answers"])
        self.assertEqual(resp["intent"], "exam_create")

    def test_rule_match_has_no_clarification(self) -> None:
        # Kural kararı yüksek-kesinliktir -> netleştirme sunmaz.
        resp = self.engine.handle({"query": "sınav nasıl oluşturulur",
                                   "session": {"role": "ogretmen", "authenticated": True}})
        self.assertIsNone(resp["clarification"])

    def test_ambiguous_query_offers_clarification(self) -> None:
        # Kısa/belirsiz sorgu -> ilk iki aday yakın -> netleştirme adayları.
        resp = self.engine.handle({"query": "yoklama nerede",
                                   "session": {"role": "ogretmen", "authenticated": True}})
        clar = resp["clarification"]
        self.assertIsNotNone(clar)
        self.assertEqual(len(clar["candidates"]), 2)
        self.assertLess(clar["margin"], 0.08)
        for cand in clar["candidates"]:
            self.assertIn("intent", cand)
            self.assertIn("label", cand)

    def test_greeting(self) -> None:
        resp = self.engine.handle({"query": "Merhaba"})
        self.assertEqual(resp["response_id"], "welcome_message")
        self.assertFalse(resp["fallback"])

    def test_trace_id_honored(self) -> None:
        resp = self.engine.handle({"query": "Merhaba", "trace_id": "abc-1"})
        self.assertEqual(resp["trace_id"], "abc-1")

    def test_trace_id_generated_when_absent(self) -> None:
        resp = self.engine.handle({"query": "Merhaba"})
        self.assertTrue(resp["trace_id"].startswith("req-"))

    def test_role_gating_in_contract(self) -> None:
        resp = self.engine.handle(
            {"query": "yeni ders oluştur", "session": {"role": "ogrenci", "authenticated": True}}
        )
        self.assertEqual(resp["intent"], "course_create")
        self.assertEqual(resp["auth_action"], "role_insufficient")
        self.assertEqual(resp["required_role"], "ogretmen")

    def test_login_required_in_contract(self) -> None:
        resp = self.engine.handle(
            {"query": "Karnemi göster", "session": {"role": "ziyaretci", "authenticated": False}}
        )
        self.assertEqual(resp["auth_action"], "login_required")

    def test_fallback(self) -> None:
        resp = self.engine.handle({"query": "qwzx plkj mnbv"})
        self.assertTrue(resp["fallback"])
        self.assertEqual(resp["response_id"], "fallback_clarification")


class ValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = Engine()

    def test_empty_query_returns_fallback(self) -> None:
        # Boş/boşluk girdi kullanıcı kaynaklıdır -> istisna değil, nazik fallback.
        resp = self.engine.handle({"query": "   "})
        self.assertTrue(resp["fallback"])
        self.assertIsNone(resp["intent"])
        self.assertEqual(resp["auth_action"], None)
        self.assertTrue(resp["text"])

    def test_missing_query_raises(self) -> None:
        # Eksik 'query' alanı sözleşme ihlalidir -> istisna kalır.
        with self.assertRaises(RequestError):
            self.engine.handle({})

    def test_unknown_role_raises(self) -> None:
        with self.assertRaises(RequestError):
            self.engine.handle({"query": "Merhaba", "session": {"role": "kral"}})

    def test_visitor_cannot_be_authenticated(self) -> None:
        with self.assertRaises(RequestError):
            self.engine.handle(
                {"query": "Merhaba", "session": {"role": "ziyaretci", "authenticated": True}}
            )


class LogSinkTests(unittest.TestCase):
    def test_log_sink_receives_trace(self) -> None:
        captured: list[dict] = []
        engine = Engine(log_sink=captured.append)
        engine.handle({"query": "Merhaba", "trace_id": "t9"})
        self.assertEqual(len(captured), 1)
        self.assertEqual(captured[0]["trace_id"], "t9")
        self.assertIn("latency_ms", captured[0])


class SharedEngineTests(unittest.TestCase):
    def test_handle_request_helper(self) -> None:
        resp = handle_request({"query": "Merhaba"})
        self.assertEqual(resp["response_id"], "welcome_message")


if __name__ == "__main__":
    unittest.main()
