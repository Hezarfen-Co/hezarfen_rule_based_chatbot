"""Cevap varyantları, selamlama aynalama ve asistan kimliği (Çelebi) testleri.

Varyant mekanizması: sosyal intent'lerde (smalltalk/thanks/farewell) aynı
response_id altında birden çok metin; seçim sorgunun CRC32'sine göre
DETERMİNİSTİK. Aynı girdi her zaman aynı cevabı alır; farklı ifadeler
farklı varyant görebilir. response_id her varyantta SABİTTİR.
"""

import unittest

from src.catalog import ASSISTANT_NAME, INTENTS, get_intent
from src.engine import Engine
from src.responder import answer
from src.safety import evaluate_input


ENGINE = Engine()


def _ask(query: str, role: str = "ogrenci") -> dict:
    return ENGINE.handle({
        "query": query,
        "session": {"role": role, "authenticated": role != "ziyaretci"},
    })


class VariantDeterminismTests(unittest.TestCase):
    def test_same_query_always_same_text(self) -> None:
        # Determinizm: aynı girdi 5 kez -> 5 kez aynı metin.
        texts = {_ask("teşekkürler")["text"] for _ in range(5)}
        self.assertEqual(len(texts), 1)

    def test_variants_share_stable_response_id(self) -> None:
        # Farklı ifadeler farklı metin alabilir ama response_id hep aynıdır.
        for query in ["teşekkürler", "sağ ol", "eyvallah", "çok teşekkür ederim"]:
            with self.subTest(query=query):
                self.assertEqual(_ask(query)["response_id"], "thanks_reply")

    def test_different_phrasings_get_different_variants(self) -> None:
        # Tekrar hissini kıran şey: ifade havuzu birden çok varyanta dağılır.
        # (CRC32 deterministik olduğundan bu dağılım sabittir; test kararlıdır.)
        thanks_texts = {_ask(q)["text"] for q in
                        ["teşekkürler", "sağ ol", "eyvallah", "çok teşekkür ederim"]}
        self.assertGreaterEqual(len(thanks_texts), 2)
        farewell_texts = {_ask(q)["text"] for q in
                          ["görüşürüz", "hoşça kal", "iyi geceler", "hoşçakalın"]}
        self.assertGreaterEqual(len(farewell_texts), 2)

    def test_every_variant_is_nonempty_and_unique(self) -> None:
        for item in INTENTS:
            variants = item.get("response_variants")
            if not variants:
                continue
            with self.subTest(intent=item["intent"]):
                pool = [item["response_template"], *variants]
                self.assertEqual(len(pool), len(set(pool)))  # kopya varyant yok
                for text in pool:
                    self.assertTrue(text.strip())

    def test_render_without_query_uses_primary_template(self) -> None:
        # query verilmezse (eski çağrı yolu) her zaman ana şablon döner.
        from src.decision import Decision
        from src.responder import render
        d = Decision(intent="thanks", fallback=False, source="rule", confidence=1.0)
        r = render(d)
        self.assertEqual(r.text, get_intent("thanks")["response_template"])


class GreetingMirrorTests(unittest.TestCase):
    """'Günaydın'a günaydın: selamlama, kullanıcının selamını aynalar."""

    def test_gunaydin_mirrored(self) -> None:
        self.assertTrue(_ask("günaydın")["text"].startswith("Günaydın!"))

    def test_iyi_gunler_mirrored(self) -> None:
        self.assertTrue(_ask("iyi günler")["text"].startswith("İyi günler!"))

    def test_selam_mirrored(self) -> None:
        self.assertTrue(_ask("selam")["text"].startswith("Selam!"))

    def test_merhaba_default(self) -> None:
        self.assertTrue(_ask("merhaba")["text"].startswith("Merhaba!"))

    def test_mirror_works_with_name_prefix(self) -> None:
        # 'çelebi günaydın' da aynalanır.
        self.assertTrue(_ask("çelebi günaydın")["text"].startswith("Günaydın!"))

    def test_responder_path_also_mirrors(self) -> None:
        # CLI yolu (responder.answer) da aynı davranır.
        self.assertTrue(answer("günaydın").text.startswith("Günaydın!"))


class AssistantIdentityTests(unittest.TestCase):
    """Asistanın adı (Çelebi) kimlik/karşılama cevaplarında geçer."""

    def test_name_constant(self) -> None:
        self.assertEqual(ASSISTANT_NAME, "Çelebi")

    def test_welcome_mentions_name(self) -> None:
        self.assertIn(ASSISTANT_NAME, _ask("merhaba")["text"])

    def test_identity_mentions_name_and_origin(self) -> None:
        text = _ask("sen kimsin")["text"]
        self.assertIn(ASSISTANT_NAME, text)
        self.assertIn("Hezarfen Ahmed Çelebi", text)  # ismin hikâyesi

    def test_name_directed_insult_is_bot_directed_not_harassment(self) -> None:
        # Bota adıyla sataşma kişiye-taciz DEĞİL: uyar ama engelleme.
        d = evaluate_input("Çelebi salak", role="ogrenci", authenticated=True)
        self.assertEqual(d.category, "PROFANITY_UNTARGETED")
        self.assertEqual(d.decision, "ALLOW_WITH_WARNING")


if __name__ == "__main__":
    unittest.main()
