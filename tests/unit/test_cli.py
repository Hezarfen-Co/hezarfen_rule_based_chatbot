"""Aşama 13 birim testleri: terminal (CLI) oturumu ve komutlar."""

import unittest

from src.cli import ChatSession, run


class SessionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.session = ChatSession()

    def test_default_role_visitor(self) -> None:
        self.assertEqual(self.session.role, "ziyaretci")
        self.assertFalse(self.session.authenticated)

    def test_set_role_valid(self) -> None:
        msg = self.session.set_role("ogretmen")
        self.assertEqual(self.session.role, "ogretmen")
        self.assertTrue(self.session.authenticated)
        self.assertIn("ogretmen", msg)

    def test_set_role_invalid(self) -> None:
        msg = self.session.set_role("kral")
        self.assertEqual(self.session.role, "ziyaretci")  # değişmez
        self.assertIn("Bilinmeyen", msg)

    def test_ask_returns_contract(self) -> None:
        resp = self.session.ask("Merhaba")
        self.assertEqual(resp["response_id"], "welcome_message")


class HandleLineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.session = ChatSession()

    def test_empty_line(self) -> None:
        text, exit_ = self.session.handle_line("   ")
        self.assertIsNone(text)
        self.assertFalse(exit_)

    def test_exit_command(self) -> None:
        text, exit_ = self.session.handle_line("/cikis")
        self.assertTrue(exit_)

    def test_role_command(self) -> None:
        text, exit_ = self.session.handle_line("/rol ogretmen")
        self.assertEqual(self.session.role, "ogretmen")
        self.assertFalse(exit_)

    def test_role_command_gating_effect(self) -> None:
        self.session.handle_line("/rol ogrenci")
        text, _ = self.session.handle_line("yeni ders oluştur")
        self.assertIn("Öğretmen", text)  # rol yetersiz uyarısı
        self.session.handle_line("/rol ogretmen")
        text2, _ = self.session.handle_line("yeni ders oluştur")
        self.assertNotIn("yetmiyor", text2)  # artık izin var

    def test_roles_command(self) -> None:
        text, _ = self.session.handle_line("/roller")
        self.assertIn("ogrenci", text)

    def test_help_command(self) -> None:
        text, _ = self.session.handle_line("/yardim")
        self.assertIn("Komutlar", text)

    def test_unknown_command(self) -> None:
        text, _ = self.session.handle_line("/bilinmeyen")
        self.assertIn("Bilinmeyen komut", text)

    def test_normal_query(self) -> None:
        text, exit_ = self.session.handle_line("Merhaba")
        self.assertIn("greeting", text)
        self.assertFalse(exit_)


class RunLoopTests(unittest.TestCase):
    def test_run_with_injected_io(self) -> None:
        inputs = iter(["Merhaba", "/rol ogretmen", "/cikis"])
        outputs: list[str] = []
        run(input_fn=lambda _prompt: next(inputs), output_fn=outputs.append)
        joined = "\n".join(outputs)
        self.assertIn("greeting", joined)
        self.assertIn("Görüşürüz", joined)

    def test_run_handles_eof(self) -> None:
        def raise_eof(_prompt: str) -> str:
            raise EOFError

        outputs: list[str] = []
        run(input_fn=raise_eof, output_fn=outputs.append)
        self.assertTrue(any("Görüşürüz" in o for o in outputs))


if __name__ == "__main__":
    unittest.main()
