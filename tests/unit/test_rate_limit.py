"""Aşama 18 birim testleri: rate-limit / spam kontrolü."""

import unittest

from src.safety import RateLimiter


class _Clock:
    def __init__(self) -> None:
        self.t = 1000.0

    def __call__(self) -> float:
        return self.t


class RateLimiterTests(unittest.TestCase):
    def test_under_limit_allows(self) -> None:
        rl = RateLimiter(max_requests=5, window_seconds=60, time_fn=_Clock())
        for i in range(5):
            self.assertIsNone(rl.check("u1", f"soru {i}"))

    def test_over_limit_blocks(self) -> None:
        clock = _Clock()
        rl = RateLimiter(max_requests=3, window_seconds=60, time_fn=clock)
        for i in range(3):
            self.assertIsNone(rl.check("u1", f"soru {i}"))
        d = rl.check("u1", "soru 4")
        self.assertIsNotNone(d)
        self.assertEqual(d.decision, "TEMPORARY_LIMIT")
        self.assertEqual(d.category, "SPAM_RATE")

    def test_window_resets(self) -> None:
        clock = _Clock()
        rl = RateLimiter(max_requests=2, window_seconds=60, time_fn=clock)
        rl.check("u1", "a")
        rl.check("u1", "b")
        clock.t += 120  # pencere geçti
        self.assertIsNone(rl.check("u1", "c"))

    def test_repeated_message_flagged(self) -> None:
        rl = RateLimiter(max_requests=100, max_repeats=3, time_fn=_Clock())
        self.assertIsNone(rl.check("u1", "aynı mesaj"))
        self.assertIsNone(rl.check("u1", "aynı mesaj"))
        d = rl.check("u1", "aynı mesaj")
        self.assertIsNotNone(d)
        self.assertEqual(d.category, "SPAM_REPEAT")

    def test_per_user_isolation(self) -> None:
        rl = RateLimiter(max_requests=2, time_fn=_Clock())
        rl.check("u1", "a")
        rl.check("u1", "b")
        # farklı kullanıcı etkilenmez
        self.assertIsNone(rl.check("u2", "a"))


class EngineRateLimitTests(unittest.TestCase):
    def test_engine_blocks_on_rate_limit(self) -> None:
        from src.engine import Engine

        rl = RateLimiter(max_requests=2, time_fn=_Clock())
        engine = Engine(rate_limiter=rl)
        payload = {"query": "Merhaba", "session": {"role": "ogrenci", "authenticated": True, "user_id": "u1"}}
        engine.handle(payload)
        engine.handle(payload)
        resp = engine.handle(payload)  # 3. istek -> limit
        self.assertEqual(resp["safety"]["decision"], "TEMPORARY_LIMIT")

    def test_engine_without_user_id_not_limited(self) -> None:
        from src.engine import Engine

        rl = RateLimiter(max_requests=1, time_fn=_Clock())
        engine = Engine(rate_limiter=rl)
        for _ in range(3):
            resp = engine.handle({"query": "Merhaba", "session": {"role": "ogrenci", "authenticated": True}})
        self.assertNotEqual(resp["safety"]["decision"], "TEMPORARY_LIMIT")


if __name__ == "__main__":
    unittest.main()
