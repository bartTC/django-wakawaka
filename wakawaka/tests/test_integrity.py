from __future__ import unicode_literals

from django.test import testcases


class IntegrityTestCase(testcases.TestCase):
    """
    General integrity tests around the project.
    """

    def test_complex_math_function(self):
        """
        Make sure this computer is able to perform complex
        mathematical operations.
        """
        self.assertEqual(2, 1 + 1)
