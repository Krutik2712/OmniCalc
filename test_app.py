import unittest
import json
from app import app
from converters import calculate, convert_unit, convert_temperature


class TestConverterLogic(unittest.TestCase):
    def test_arithmetic(self):
        # Addition
        res, expr = calculate("add", 10, 5)
        self.assertEqual(res, 15)
        self.assertIn("10 + 5", expr)

        # Subtraction
        res, _ = calculate("subtract", 20, 7)
        self.assertEqual(res, 13)

        # Multiplication
        res, _ = calculate("multiply", 6, 7)
        self.assertEqual(res, 42)

        # Division
        res, _ = calculate("divide", 50, 2)
        self.assertEqual(res, 25)

        # Power
        res, _ = calculate("power", 2, 8)
        self.assertEqual(res, 256)

        # Square root
        res, _ = calculate("sqrt", 81)
        self.assertEqual(res, 9)

        # Modulo
        res, _ = calculate("modulo", 17, 5)
        self.assertEqual(res, 2)

    def test_arithmetic_errors(self):
        # Division by zero
        with self.assertRaises(ValueError):
            calculate("divide", 10, 0)

        # Modulo by zero
        with self.assertRaises(ValueError):
            calculate("modulo", 10, 0)

        # Sqrt of negative
        with self.assertRaises(ValueError):
            calculate("sqrt", -9)

    def test_temperature_conversion(self):
        # 0 C -> 32 F
        f = convert_temperature(0, "celsius", "fahrenheit")
        self.assertAlmostEqual(f, 32.0, places=2)

        # 100 C -> 212 F
        f = convert_temperature(100, "celsius", "fahrenheit")
        self.assertAlmostEqual(f, 212.0, places=2)

        # 0 C -> 273.15 K
        k = convert_temperature(0, "celsius", "kelvin")
        self.assertAlmostEqual(k, 273.15, places=2)

        # 32 F -> 0 C
        c = convert_temperature(32, "fahrenheit", "celsius")
        self.assertAlmostEqual(c, 0.0, places=2)

    def test_unit_conversions(self):
        # Length: 1 km -> 1000 m
        res, _ = convert_unit("length", 1, "kilometers", "meters")
        self.assertEqual(res, 1000)

        # Length: 1 meter -> ~3.28084 feet
        res, _ = convert_unit("length", 1, "meters", "feet")
        self.assertAlmostEqual(res, 3.28084, places=4)

        # Weight: 1 kg -> ~2.20462 lbs
        res, _ = convert_unit("weight", 1, "kilograms", "pounds")
        self.assertAlmostEqual(res, 2.20462, places=3)

        # Digital Data: 1024 MB -> 1 GB
        res, _ = convert_unit("data", 1024, "megabytes", "gigabytes")
        self.assertEqual(res, 1.0)


class TestFlaskEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"OmniCalc & Unit Hub", response.data)

    def test_api_units(self):
        response = self.client.get("/api/units")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertIn("length", data["categories"])

    def test_api_calculate_success(self):
        payload = {"operation": "multiply", "num1": 12, "num2": 8}
        response = self.client.post(
            "/api/calculate",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertEqual(data["result"], 96)

    def test_api_calculate_div_zero(self):
        payload = {"operation": "divide", "num1": 50, "num2": 0}
        response = self.client.post(
            "/api/calculate",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data["success"])
        self.assertIn("zero", data["error"].lower())

    def test_api_convert_success(self):
        payload = {
            "category": "temperature",
            "value": 100,
            "from_unit": "celsius",
            "to_unit": "fahrenheit"
        }
        response = self.client.post(
            "/api/convert",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertEqual(data["result"], 212)


if __name__ == "__main__":
    unittest.main()
