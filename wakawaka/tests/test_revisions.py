from __future__ import unicode_literals

from django.urls import reverse

from wakawaka.tests.base import BaseTestCase


class RevisionsTestCase(BaseTestCase):
    """
    The Revisions view displays the list of revisions of a given page.
    """

    def test_revisions(self):
        """
        Calling the revisions view without a slug, displays all
        revisions of all pages.
        """
        # Create a couple of Wiki pages
        self.create_wikipage('WikiIndex', 'First Content', 'Second Content')
        self.create_wikipage('CarrotCake', 'Carrot Content')

        response = self.client.get(reverse('wakawaka_revision_list'))
        self.assertContains(response, 'Created via API: First Content')
        self.assertContains(response, 'Created via API: Second Content')
        self.assertContains(response, 'Created via API: Carrot Content')

    def test_revisions_for_slug(self):
        """
        Calling the Revisions View with a slug will only display the
        revisions of this page.
        """
        # Create a couple of Wiki pages
        self.create_wikipage('WikiIndex', 'First Content', 'Second Content')
        self.create_wikipage('CarrotCake', 'Carrot Content')

        response = self.client.get(reverse('wakawaka_revision_list',
                                           kwargs={'slug': 'WikiIndex'}))
        self.assertContains(response, 'Created via API: First Content')
        self.assertContains(response, 'Created via API: Second Content')
        self.assertNotContains(response, 'Created via API: Carrot Content')
