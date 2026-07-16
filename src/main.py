"""Container giriş noktası ve katalog doğrulaması."""

from __future__ import annotations

import argparse
from typing import Any

from .catalog import validate_catalog


def print_validation_result(result: dict[str, Any]) -> None:
    """Kısa, log dostu bir doğrulama sonucu yazdırır."""

    print("Katalog doğrulandı.")
    print(f"Intent: {result['intent_count']}")
    print(f"Cevap: {result['response_count']}")
    print(f"Kategori: {result['category_count']}")
    print(f"Örnek soru: {result['example_question_count']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Hezarfen kullanım asistanı chatbot'u")
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Intent kataloğunu doğrular ve çıkar.",
    )
    parser.add_argument(
        "--evaluate",
        action="store_true",
        help="Benchmark üzerinde tam değerlendirme raporu üretir.",
    )
    parser.add_argument(
        "--chat",
        action="store_true",
        help="Etkileşimli terminal sohbetini başlatır.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.chat:
        from .cli import main as chat_main

        return chat_main()

    if args.evaluate:
        from .evaluate import format_report, run_evaluation

        print(format_report(run_evaluation()))
        return 0

    if args.validate:
        print_validation_result(validate_catalog())
        return 0

    # Motor eklenene kadar çıplak çalıştırma da güvenli bir doğrulama yapar.
    print_validation_result(validate_catalog())
    print("Chatbot motoru henüz eklenmedi.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
