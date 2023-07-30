import unittest

from fastapi.testclient import TestClient

from main import get_application


class TestJsonToXmlService(unittest.TestCase):
    def setUp(self):
        self.app = TestClient(get_application())

    def test_valid_json_to_xml(self):
        json_data = {"name": "John", "age": 30, "arr": [1,2,3,4,5], "money":2234.23, "at_date": "23.12.2023"}
        response = self.app.post("/transfer_json_to_xml", json=json_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<name type="str">John</name>', response.text)
        self.assertIn('<age type="int">30</age>', response.text)

    def test_empty_json_to_xml(self):
        empty_json_data = {}
        response = self.app.post("/transfer_json_to_xml", json=empty_json_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text.strip('"'), '<?xml version=\\"1.0\\" ?><metadata></metadata>')

    def test_invalid_json_data(self):
        invalid_json_data = "invalid_json"
        response = self.app.post("/transfer_json_to_xml", json=invalid_json_data)
        self.assertEqual(response.status_code, 422)
 
 
if __name__ == "__main__":
    unittest.main()