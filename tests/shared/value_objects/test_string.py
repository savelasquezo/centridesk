from django.test import SimpleTestCase

from shared.exceptions.required_value import RequiredValue
from shared.exceptions.too_long_string import TooLongString
from shared.exceptions.type_error import TypeErrorValue
from shared.infrastructure.b64 import encode_obj
from shared.value_objects.string import String


class TestString(SimpleTestCase):

    def test_string_correct_format(self):
        string = "Centribal"
        self.assertEqual(String(name='string', value=string, required=False).value, string)

    def test_string_correct_format_encode(self):
        string = "Centribal"
        self.assertEqual(String(name='string', value=string, required=False).encoded, encode_obj(string))

    def test_string_none(self):
        self.assertEqual(String(name='string', value=None, required=False).value, None)

    def test_string_wrong_format(self):
        try:
            String(name='string', value=12345)
        except TypeErrorValue as e:
            self.assertEqual(e.message, "String has an invalid type.")

    def test_string_empty_string(self):
        try:
            String(name='string', value="  ")
        except RequiredValue as e:
            self.assertEqual(e.message, "String is required")

    def test_string_too_long(self):
        try:
            String(name='string', value='Test', max_characters=2)
        except TooLongString as e:
            self.assertEqual(e.message, f"String exceed the number of characters. Max: 2.")

    def test_string_required(self):
        try:
            String(name='string', value=None, required=True)
        except RequiredValue as e:
            self.assertEqual(e.message, f"String is required")
