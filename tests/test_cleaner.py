"""
Unit test suite for cleanjson.
"""

import unittest
from cleanjson import clean, Cleaner


class TestCleanJson(unittest.TestCase):

    def test_user_requested_example(self):
        data = {
            "name": "  Hamdan  ",
            "email": " HAMDAN@GMAIL.COM ",
            "age": "21"
        }
        result = clean(data)
        expected = {
            "name": "Hamdan",
            "email": "hamdan@gmail.com",
            "age": 21
        }
        self.assertEqual(result, expected)

    def test_whitespace_and_key_trimming(self):
        data = {"  first_name  ": "  Alice  ", "items": ["  apple ", " banana "]}
        result = clean(data)
        self.assertEqual(result, {"first_name": "Alice", "items": ["apple", "banana"]})

    def test_email_normalization(self):
        data = {
            "user_email": " USER@EXAMPLE.COM ",
            "contact": "info@DOMAIN.ORG",
            "not_email": "just text"
        }
        result = clean(data)
        self.assertEqual(result["user_email"], "user@example.com")
        self.assertEqual(result["contact"], "info@domain.org")
        self.assertEqual(result["not_email"], "just text")

    def test_phone_normalization(self):
        data = {
            "phone": "+1 (555) 123-4567",
            "mobile": "555.987.6543",
        }
        result = clean(data)
        self.assertEqual(result["phone"], "+15551234567")
        self.assertEqual(result["mobile"], "5559876543")

    def test_type_conversion(self):
        data = {
            "integer": "42",
            "negative_int": "-100",
            "float_num": "3.14159",
            "is_valid": "true",
            "is_admin": "false",
            "regular_str": "hello 123"
        }
        result = clean(data)
        self.assertEqual(result["integer"], 42)
        self.assertEqual(result["negative_int"], -100)
        self.assertEqual(result["float_num"], 3.14159)
        self.assertEqual(result["is_valid"], True)
        self.assertEqual(result["is_admin"], False)
        self.assertEqual(result["regular_str"], "hello 123")

    def test_list_deduplication(self):
        data = {
            "numbers": ["1", "2", "2", "3", "1"],
            "tags": ["a", "b", "a", "c"]
        }
        result = clean(data)
        self.assertEqual(result["numbers"], [1, 2, 3])
        self.assertEqual(result["tags"], ["a", "b", "c"])

    def test_drop_empty(self):
        data = {
            "name": "Bob",
            "empty_str": "   ",
            "null_val": None,
            "empty_list": [],
            "empty_dict": {}
        }
        result = clean(data, drop_empty=True)
        self.assertEqual(result, {"name": "Bob"})

    def test_nested_structures(self):
        data = {
            "user": {
                "details": {
                    "email": " TEST@NESTED.COM ",
                    "scores": ["10", "20", "10"]
                }
            }
        }
        result = clean(data)
        self.assertEqual(
            result,
            {
                "user": {
                    "details": {
                        "email": "test@nested.com",
                        "scores": [10, 20]
                    }
                }
            }
        )

    def test_custom_rules(self):
        data = {"code": "  xyz-123  "}
        result = clean(data, custom_rules={"code": lambda x: x.strip().upper()})
        self.assertEqual(result, {"code": "XYZ-123"})


if __name__ == "__main__":
    unittest.main()
