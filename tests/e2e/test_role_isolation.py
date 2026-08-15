"""Rol izolasyonu sözleşmesi: her rolün AYRI cevap uzayı.

Bu dosya kullanıcının çekirdek şartını sabitler:
  1) Nerede ne cevap veriliyor — izinli rol adımları görür.
  2) Bir rolün cevabı diğerine SIZMAZ — düşük rol, ayrıcalıklı bir işlemi
     sorunca adım/rota/ayrıcalıklı-rol-adı ASLA görmez (yalnız kibar ret).
  3) Bilmiyorsa — kapsam dışı/belirsiz sorguda "anlayamadım, bunu mu demek
     istedin?" + aynı rol uzayından öneriler döner.

Model ikili: ALLOW (adım + yönlendirme) / DENY (kibar ret, sızıntı yok).
Kapsam (kendi/yönetilen/bağlı) cevabın içinde nottur, ayrı bir outcome değildir.
"""

import unittest

from src.engine import Engine


ENGINE = Engine()


def ask(query: str, role: str) -> dict:
    return ENGINE.handle(
        {"query": query, "session": {"role": role, "authenticated": role != "ziyaretci"}}
    )


# (sorgu, o işlemi YAPAMAYAN roller, YAPABİLEN bir rol)
CROSS_ROLE: list[tuple[str, list[str], str]] = [
    ("sınav oluşturmak istiyorum", ["ogrenci", "veli"], "ogretmen"),
    ("kullanıcı rolünü değiştirmek istiyorum", ["ogrenci", "ogretmen", "yonetici"], "admin"),
    ("okul ayarlarını değiştirmek istiyorum", ["ogrenci", "ogretmen"], "yonetici"),
    ("personel mesailerini görmek istiyorum", ["ogrenci", "ogretmen"], "yonetici"),
    ("bir öğrencinin karnesine bakmak istiyorum", ["ogrenci"], "ogretmen"),
]

# Cevap gövdesinde ASLA görünmemesi gereken, o işlemin adımlarına/rotasına özgü
# imza ifadeler (sızıntı dedektörü).
STEP_SIGNATURES: dict[str, list[str]] = {
    "sınav oluşturmak istiyorum": ["Sınav oluştur", "Ders seç", "/exams"],
    "kullanıcı rolünü değiştirmek istiyorum": ["/admin/users", "rol menüsünden"],
    "okul ayarlarını değiştirmek istiyorum": ["/management/settings", "Not bantları"],
    "personel mesailerini görmek istiyorum": ["/management/staff-work", "Düzenle"],
    "bir öğrencinin karnesine bakmak istiyorum": ["/management/student-marks"],
}


class CrossRoleIsolationTests(unittest.TestCase):
    """Yasak rol: adım/rota/ayrıcalıklı-rol-adı sızmaz; izinli rol: gerçek adım+rota."""

    def test_denied_role_gets_no_steps_or_route(self) -> None:
        for query, forbidden_roles, _allowed in CROSS_ROLE:
            for role in forbidden_roles:
                with self.subTest(query=query, role=role):
                    resp = ask(query, role)
                    self.assertIsNotNone(resp["auth_action"])  # reddedildi
                    self.assertIsNone(resp["navigation"])       # rota sızmadı
                    for sig in STEP_SIGNATURES[query]:
                        self.assertNotIn(sig, resp["text"])     # adım/rota sızmadı

    def test_allowed_role_gets_steps_and_route(self) -> None:
        for query, _forbidden, allowed in CROSS_ROLE:
            with self.subTest(query=query, role=allowed):
                resp = ask(query, allowed)
                self.assertIsNone(resp["auth_action"])          # izinli
                self.assertIsNotNone(resp["navigation"])         # yönlendirme var


# Ortak sorular: her rol uzayında bulunmalı (fallback değil, izinli).
COMMON_QUERIES = ["merhaba", "teşekkürler", "roller ve yetkiler nedir", "mesajlarım nerede"]


class CommonSpaceTests(unittest.TestCase):
    """Ortak sorular her rol uzayında yanıtlanır (kopya-paste değil, derlenmiş)."""

    def test_common_questions_answered_in_every_role_space(self) -> None:
        for role in ("veli", "ogrenci", "ogretmen", "yonetici", "admin"):
            for query in COMMON_QUERIES:
                with self.subTest(role=role, query=query):
                    resp = ask(query, role)
                    self.assertFalse(resp["fallback"])
                    self.assertIsNone(resp["auth_action"])


class OutOfScopeSuggestionTests(unittest.TestCase):
    """Bilmiyorsa: 'anlayamadım, bunu mu?' + aynı uzaydan aday öneriler."""

    def test_ambiguous_offers_clarification_with_candidates(self) -> None:
        resp = ask("bir yerde hata verdi yardım et", "ogrenci")
        self.assertEqual(resp["response_id"], "clarification_prompt")
        self.assertIn("anlayamadım", resp["text"])
        clar = resp["clarification"]
        self.assertIsNotNone(clar)
        self.assertEqual(len(clar["candidates"]), 2)
        for cand in clar["candidates"]:
            self.assertTrue(cand["intent"])

    def test_out_of_domain_falls_back_without_inventing(self) -> None:
        for query in ["bugün hava nasıl", "dolar kaç lira"]:
            with self.subTest(query=query):
                resp = ask(query, "ogrenci")
                self.assertTrue(resp["fallback"])


if __name__ == "__main__":
    unittest.main()
