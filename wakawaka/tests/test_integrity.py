from __future__ import unicode_literals

from django import get_version
from django.test import testcases
from django.core.urlresolvers import reverse
from distutils.version import StrictVersion

DJANGO_VERSION = get_version()

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

    def test_calling_home_redircts_to_wikiindex(self):
        """
        Calling the homepage `/` will automatically redirect to the
        `WikiIndex` index page.
        """
        response = self.client.get(reverse('wakawaka_index'))
        self.assertEqual(response.status_code, 302)

        if StrictVersion(DJANGO_VERSION) >= StrictVersion('1.9'):
            self.assertEqual(response['Location'], '/WikiIndex/')
        else:
            self.assertEqual(response['Location'], 'http://testserver/WikiIndex/')

    def test_wikiindex_is_a_setting(self):
        """
        This Homepage name `WikiIndex` can be set by a setting.
        """
        with self.settings(WAKAWAKA_DEFAULT_INDEX='WikiWukuIndex'):
            response = self.client.get(reverse('wakawaka_index'))
            self.assertEqual(response.status_code, 302)

        if StrictVersion(DJANGO_VERSION) >= StrictVersion('1.9'):
            self.assertEqual(response['Location'], '/WikiWukuIndex/')
        else:
            self.assertEqual(response['Location'], 'http://testserver/WikiWukuIndex/')
