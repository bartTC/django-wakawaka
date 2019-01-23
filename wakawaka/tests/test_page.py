from __future__ import unicode_literals

from django.contrib.auth.models import Permission
from django.urls import reverse

from wakawaka.forms import WikiPageForm
from wakawaka.models import WikiPage, Revision
from wakawaka.tests.base import BaseTestCase


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
        self.login_superuser()

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
        self.login_superuser()

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
        self.create_wikipage('WikiIndex', 'Some content')

        data = {'content': 'This is updated content.'}
        edit_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex'})
        page_perm = Permission.objects.get(codename='change_wikipage')
        rev_perm = Permission.objects.get(codename='change_revision')

        # Login a user with no permissions
        user = self.login_staffuser_noperm()

        # User with no perm can't edit
        response = self.client.post(edit_url, data, follow=True)
        self.assertEqual(response.status_code, 403)

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

    def test_edit_page_with_same_content_does_not_work(self):
        """
        Saving a page revision with the same content as before, won't create a
        new revision.
        """
        self.login_superuser()

        data1 = {'content': 'First Content'}
        edit_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex'})
        self.client.post(edit_url, data1, follow=True)

        data2 = {'content': 'First Content'}
        edit_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex'})
        self.client.post(edit_url, data2, follow=True)

        self.assertEqual(WikiPage.objects.count(), 1)
        self.assertEqual(WikiPage.objects.all()[0].revisions.count(), 1)
        self.assertEqual(Revision.objects.count(), 1)

    def test_edit_revision_reverts_content(self):
        """
        If the user calls the revision edit page form, and submits it, it
        will automatically revert the content to this revision.
        """
        # Create a WikiIndex page with two revisions:
        rev1 = 'First Content'
        rev2 = 'Updated Content'
        self.create_wikipage('WikiIndex', rev1, rev2)

        # Need to be logged in to edit a Page
        self.login_superuser()

        # Calling edit form with older revision will have that content in form
        page_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex', 'rev_id': 1})
        response = self.client.get(page_url, follow=True)
        self.assertContains(response, rev1)
        self.assertContains(response, 'Reverted')
        # @OPTIMIZE: should not test for "Reverted" in text, too vague

        # Calling the edit form of the current revision, will display the regular
        # edit form.
        page_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex', 'rev_id': 2})
        response = self.client.get(page_url, follow=True)
        self.assertContains(response, rev2)
        self.assertNotContains(response, 'Reverted')
        # @OPTIMIZE: should not test for "Reverted" in text, too vague

    # --------------------------------------------------------------------------
    # Page deletion
    # --------------------------------------------------------------------------
    def test_user_needs_delete_perm_for_page(self):
        """
        Deleting an entire page needs both 'delete_revision' and 'delete_wikipage'
        permission.

        The delete form is integrated into the edit page. It's a choicefield
        holding either or both of 'rev' and 'page' depending on the users
        permission.
        """
        # Create one page with two revisions upfront
        self.create_wikipage('WikiIndex', 'Some content', 'Other content')
        self.assertEqual(WikiPage.objects.count(), 1)
        self.assertEqual(Revision.objects.count(), 2)

        # Need to be logged in to edit a Page. The user also needs edit
        # permission to see the edit page
        user = self.login_staffuser_noperm()
        user.user_permissions.add(Permission.objects.get(codename='change_wikipage'))
        user.user_permissions.add(Permission.objects.get(codename='change_revision'))

        # The user has no permission at all so this will fail. The delete
        # form is not even displayed then. So this is silently ignored,
        data = {'delete': 'rev'}
        page_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex', 'rev_id': 2})
        self.client.post(page_url, data, follow=False)
        self.assertEqual(WikiPage.objects.count(), 1)
        self.assertEqual(Revision.objects.count(), 2)

        # Give the user delete_revision permission so they can delete it.
        user.user_permissions.add(Permission.objects.get(codename='delete_revision'))

        data = {'delete': 'rev'}
        page_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex', 'rev_id': 2})
        self.client.post(page_url, data, follow=True)

        self.assertEqual(WikiPage.objects.count(), 1)
        self.assertEqual(Revision.objects.count(), 1)

        # If a page has only one Revision set, and the user tries to delete
        # this revision, it will also delete the page - but only if the user
        # has aside 'delete_revision' permission also 'delete_wikipage' permission.
        data = {'delete': 'rev'}
        page_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex', 'rev_id': 1})
        self.client.post(page_url, data, follow=True)

        self.assertEqual(WikiPage.objects.count(), 1)
        self.assertEqual(Revision.objects.count(), 1)

        # Give the user delete_wikipage permission so they can delete the
        # entire page, by deleting the last revision of it
        user.user_permissions.add(Permission.objects.get(codename='delete_wikipage'))

        data = {'delete': 'rev'}
        page_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex', 'rev_id': 1})
        self.client.post(page_url, data, follow=True)

        # Since the page does not exist anymore, the user is redirected to
        # the index page.
        self.assertEqual(WikiPage.objects.count(), 0)
        self.assertEqual(Revision.objects.count(), 0)

    def test_delete_page(self):
        """
        If the user has all permissions they can delete the page right away.
        """
        user = self.login_staffuser_noperm()
        user.user_permissions.add(Permission.objects.get(codename='change_wikipage'))
        user.user_permissions.add(Permission.objects.get(codename='change_revision'))
        user.user_permissions.add(Permission.objects.get(codename='delete_wikipage'))
        user.user_permissions.add(Permission.objects.get(codename='delete_revision'))

        # Create one page with two revisions upfront
        self.create_wikipage('WikiIndex', 'Some content', 'Other content')
        self.assertEqual(WikiPage.objects.count(), 1)
        self.assertEqual(Revision.objects.count(), 2)

        data = {'delete': 'page'}
        page_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex'})
        self.client.post(page_url, data, follow=False)
        self.assertEqual(WikiPage.objects.count(), 0)
        self.assertEqual(Revision.objects.count(), 0)

    def test_delete_bad_value(self):
        """
        Deleting a page or revision still needs to be set. If the delete form
        passes no or an invalid value, nothing happens.
        """
        user = self.login_staffuser_noperm()
        user.user_permissions.add(Permission.objects.get(codename='change_wikipage'))
        user.user_permissions.add(Permission.objects.get(codename='change_revision'))
        user.user_permissions.add(Permission.objects.get(codename='delete_wikipage'))
        user.user_permissions.add(Permission.objects.get(codename='delete_revision'))

        # Create one page with two revisions upfront
        self.create_wikipage('WikiIndex', 'Some content', 'Other content')
        self.assertEqual(WikiPage.objects.count(), 1)
        self.assertEqual(Revision.objects.count(), 2)

        # No value
        data = {'delete': ''}
        page_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex'})
        self.client.post(page_url, data, follow=False)
        self.assertEqual(WikiPage.objects.count(), 1)
        self.assertEqual(Revision.objects.count(), 2)

        # Invalid value
        data = {'delete': 'foobar'}
        page_url = reverse('wakawaka_edit', kwargs={'slug': 'WikiIndex'})
        self.client.post(page_url, data, follow=False)
        self.assertEqual(WikiPage.objects.count(), 1)
        self.assertEqual(Revision.objects.count(), 2)
