from __future__ import unicode_literals

from django import get_version
from django.contrib.auth.models import User
from django.test import testcases
from django.core.urlresolvers import reverse
from distutils.version import StrictVersion

from wakawaka.forms import WikiPageForm
from wakawaka.models import WikiPage

DJANGO_VERSION = get_version()

class WakaWakaTestCase(testcases.TestCase):
    """
    General integrity tests around the project.
    """
    def create_superuser(self, username='superuser', password='foobar'):
        return User.objects.create_superuser(
            username, '{}@example.com'.format(username), password)

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

    def test_if_user_logged_in_page_form_is_displayed(self):
        """
        If a user is logged in, we redirect to a Create Page form.
        """
        user = self.create_superuser()
        self.client.force_login(user)

        # Calling /WikiIndex/ will result in a redirect to /edit/
        response = self.client.get(reverse('wakawaka_index'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue(isinstance(response.context['form'], WikiPageForm))

    def test_pageform_invalid(self):
        """
        At a bare minimum, the PageForm needs a 'content' field. Otherwise
        the form is displayed again, having errors.
        """
        user = self.create_superuser()
        self.client.force_login(user)

        data = {}
        edit_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex'})
        response = self.client.post(edit_url, data, follow=True)
        self.assertTrue('form' in response.context)
        self.assertTrue(isinstance(response.context['form'], WikiPageForm))

    def test_pageform_valid(self):
        """
        Having a valid 'content' POST object will create that page.
        :return:
        """
        content = 'This is the content of the new WikiIndex page'
        formatted = '<p>This is the content of the new <a href="/WikiIndex/">WikiIndex</a> page</p>'

        user = self.create_superuser()
        self.client.force_login(user)

        data = {'content': content}
        edit_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex'})
        response = self.client.post(edit_url, data, follow=True)

        # The Response is our page, and it has the content formatted in it.
        # Since WikiIndex is a valid Page index word, it's linked automatically.
        self.assertContains(response, formatted)

        # One Page with one revision was created
        self.assertEqual(WikiPage.objects.count(), 1)
        self.assertEqual(WikiPage.objects.all()[0].revisions.count(), 1)
