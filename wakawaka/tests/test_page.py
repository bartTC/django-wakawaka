from __future__ import unicode_literals

from django import get_version
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse

from wakawaka.forms import WikiPageForm
from wakawaka.models import WikiPage, Revision
from wakawaka.tests.base import BaseTestCase

DJANGO_VERSION = get_version()


class PageTestCase(BaseTestCase):
    """
    Wiki Page display, editing and deleting.
    """
    def test_if_user_not_logged_in_404(self):
        """
        Pages which don't exist, and the user is not logged in, display 404.
        """
        response = self.client.get(reverse('wakawaka_index'), follow=True)
        self.assertEqual(response.status_code, 404)

    def test_if_user_logged_in_page_form_is_displayed(self):
        """
        If a user is logged in, and the page does not exist yet, we redirect
        to a Create Page form.
        """
        user = self.login_superuser()

        # Calling /WikiIndex/ will result in a redirect to /edit/
        response = self.client.get(reverse('wakawaka_index'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue(isinstance(response.context['form'], WikiPageForm))

    # --------------------------------------------------------------------------
    # Page form creation and permissions
    # --------------------------------------------------------------------------

    def test_page_form_invalid(self):
        """
        At a bare minimum, the PageForm needs a 'content' field. Otherwise
        the form is displayed again, having errors.
        """
        user = self.login_superuser()

        data = {}
        edit_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex'})
        response = self.client.post(edit_url, data, follow=True)
        self.assertTrue('form' in response.context)
        self.assertTrue(isinstance(response.context['form'], WikiPageForm))

    def test_page_form_valid(self):
        """
        Having a valid 'content' POST object will create that page.
        """
        content = 'This is the content of the new WikiIndex page'
        formatted = '<p>This is the content of the new <a href="/WikiIndex/">WikiIndex</a> page</p>'

        self.login_superuser()

        data = {'content': content}
        edit_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex'})
        response = self.client.post(edit_url, data, follow=True)

        # The Response is our page, and it has the content formatted in it.
        # Since WikiIndex is a valid Page index word, it's linked automatically.
        self.assertContains(response, formatted)

        # One Page with one revision was created
        self.assertEqual(WikiPage.objects.count(), 1)
        self.assertEqual(WikiPage.objects.all()[0].revisions.count(), 1)

    def test_page_add_only_if_perm(self):
        """
        The user needs 'add_wikipage' and 'add_revision' permission to add
        add a page.
        """
        user = self.login_staffuser_noperm()

        # No permission
        data = {'content': 'This is the content of the new WikiIndex page'}
        edit_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex'})
        response = self.client.post(edit_url, data, follow=True)
        self.assertEqual(response.status_code, 403)

        page_perm = Permission.objects.get(codename='add_wikipage')
        rev_perm = Permission.objects.get(codename='add_revision')

        # Just the page perm is not enough
        user.user_permissions.add(page_perm)
        response = self.client.post(edit_url, data, follow=True)
        self.assertEqual(response.status_code, 403)

        # Page perm and rev perm is ok
        user.user_permissions.add(rev_perm)
        response = self.client.post(edit_url, data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_page_edit_only_if_perm(self):
        """
        Users need at least 'wakawaka.change_wikipage' and
        'wakawaka.change_revision' permission to edit a page.
        """
        # Create page upfront
        self.login_superuser()
        data = {'content': 'This is the content of the new WikiIndex page'}
        edit_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex'})
        self.client.post(edit_url, data, follow=True)

        # User with no perm can't edit
        user = self.login_staffuser_noperm()
        response = self.client.post(edit_url, data, follow=True)
        self.assertEqual(response.status_code, 403)

        page_perm = Permission.objects.get(codename='change_wikipage')
        rev_perm = Permission.objects.get(codename='change_revision')

        # Just the page perm is not enough
        user.user_permissions.add(page_perm)
        response = self.client.post(edit_url, data, follow=True)
        self.assertEqual(response.status_code, 403)

        # Page perm and rev perm is ok
        user.user_permissions.add(rev_perm)
        response = self.client.post(edit_url, data, follow=True)
        self.assertEqual(response.status_code, 200)

    # --------------------------------------------------------------------------
    # Page revisions
    # --------------------------------------------------------------------------

    def test_editing_again_creates_revision(self):
        """
        Submitting a page edit form multiple times creates a separate revision
        automatically.
        """
        self.login_superuser()

        data1 = {'content': 'First Content'}
        edit_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex'})
        self.client.post(edit_url, data1, follow=True)

        data2 = {'content': 'Updated Content'}
        edit_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex'})
        self.client.post(edit_url, data2, follow=True)

        # One Page with one revision was created
        self.assertEqual(WikiPage.objects.count(), 1)
        self.assertEqual(WikiPage.objects.all()[0].revisions.count(), 2)

        # We can call each revision individually. The last change is displayed
        # when calling without a revision
        page_url = reverse('wakawaka_page', kwargs={'slug': 'WikiIndex'})
        response = self.client.get(page_url, follow=True)
        self.assertContains(response, data2['content'])

        page_url = reverse('wakawaka_page', kwargs={'slug': 'WikiIndex', 'rev_id': 2})
        response = self.client.get(page_url, follow=True)
        self.assertContains(response, data2['content'])

        page_url = reverse('wakawaka_page', kwargs={'slug': 'WikiIndex', 'rev_id': 1})
        response = self.client.get(page_url, follow=True)
        self.assertContains(response, data1['content'])

    def test_edit_revision_reverts_content(self):
        """
        If the user calls the revision edit page form, and submits it, it
        will automatically revert the content to this revision.
        """
        self.login_superuser()

        data1 = {'content': 'First Content'}
        edit_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex'})
        self.client.post(edit_url, data1, follow=True)

        data2 = {'content': 'Updated Content'}
        edit_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex'})
        self.client.post(edit_url, data2, follow=True)

        # Calling edit form with older revision will have that content in form
        page_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex', 'rev_id': 1})
        response = self.client.get(page_url, follow=True)
        self.assertContains(response, data1['content'])
        self.assertContains(response, 'Reverted')
        # @OPTIMIZE: should not test for "Reverted" in text, too vague

        # Calling the edit form of the current revision, will display the regular
        # edit form.
        page_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex', 'rev_id': 2})
        response = self.client.get(page_url, follow=True)
        self.assertContains(response, data2['content'])
        self.assertNotContains(response, 'Reverted')
        # @OPTIMIZE: should not test for "Reverted" in text, too vague

    # --------------------------------------------------------------------------
    # Page deletion
    # --------------------------------------------------------------------------

    def test_user_needs_delete_perm(self):
        """
        Deleting a page is done by calling the edit view, with a 'delete=True'
        Post value. User needs to have all of change and delete permission for
        WikiPage and Revision
        """
        pass

    def test_user_can_delete_revision(self):
        pass
