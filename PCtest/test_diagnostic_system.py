import unittest
from diagnostic_system import DiagnosticSystem

class TestDiagnosticSystem(unittest.TestCase):
    def setUp(self):
        self.ds = DiagnosticSystem(csv_path=":memory:")  # використаємо тимчасовий файл

    def test_power_and_fans_failure(self):
        data = {"power": False, "fans": False, "temp": 0, "noise": False}
        result = self.ds.diagnose(data)
        self.assertIn("Можливо, несправний блок живлення", result)

    def test_cooling_issue(self):
        data = {"power": True, "fans": False, "temp": 75, "noise": True}
        result = self.ds.diagnose(data)
        self.assertIn("Перегрів системи охолодження", result)

    def test_no_disk_noise(self):
        data = {"power": True, "fans": True, "temp": 40, "noise": False}
        result = self.ds.diagnose(data)
        self.assertIn("Можливо, не працює накопичувач", result)

    def test_critical_overheat(self):
        data = {"power": True, "fans": True, "temp": 95, "noise": True}
        result = self.ds.diagnose(data)
        self.assertIn("Критичний перегрів", result)

    def test_unknown_case(self):
        data = {"power": True, "fans": True, "temp": 45, "noise": True}
        result = self.ds.diagnose(data)
        self.assertEqual(result, ["Невідомо"])

    def test_invalid_temperature(self):
        data = {"power": True, "fans": True, "temp": "гаряче", "noise": True}
        with self.assertRaises(ValueError):
            self.ds.diagnose(data)

if __name__ == "__main__":
    unittest.main()
