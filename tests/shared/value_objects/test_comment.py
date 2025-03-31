import unittest

from shared.exceptions.required_value import RequiredValue
from shared.exceptions.type_error import TypeErrorValue
from shared.value_objects.comment import CommentBody


class TestComment(unittest.TestCase):

    def test_not_empty(self):
        try:
            CommentBody('')
        except RequiredValue as ex:
            self.assertEqual(ex.message, 'Text is required')

    def test_required(self):
        try:
            CommentBody(None)
        except RequiredValue as ex:
            self.assertEqual(ex.message, 'Text is required')

    def test_must_be_str(self):
        try:
            CommentBody(5)
        except TypeErrorValue as ex:
            self.assertEqual(ex.message, "Text has an invalid type.")

    def test_set_ok(self):
        self.assertEqual(CommentBody('Text').text, 'Text')
