from django.urls import reverse

from wakawaka.tests.base import BaseTestCase


class PageListTestCase(BaseTestCase):
    """
    The Revision List displays all Pages.
    """

    def test_pagelist(self):
        # Create a couple of Wiki pages
        self.create_wikipage("WikiIndex", "Some content")
        self.create_wikipage("CarrotCake", "Some content")
        self.create_wikipage("BeanSoup", "Some content")

        response = self.client.get(reverse("wakawaka_page_list"))
        self.assertContains(response, "WikiIndex")
        self.assertContains(response, "CarrotCake")
        self.assertContains(response, "BeanSoup")
