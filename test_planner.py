import unittest

from planner import SCHEDULES, make_plan


class TestPlanner(unittest.TestCase):
    def test_sums(self):
        for duration, blocks in SCHEDULES.items():
            self.assertEqual(sum(n for n, _ in blocks), duration)
            self.assertIn(f"Duración total: {duration} minutos", make_plan("Álgebra", duration))

    def test_invalid_topic(self):
        for topic in ["", "x", "x" * 81]:
            with self.assertRaises(ValueError):
                make_plan(topic, 30)

    def test_invalid_duration(self):
        with self.assertRaises(ValueError):
            make_plan("Historia", 45)


if __name__ == "__main__":
    unittest.main()
