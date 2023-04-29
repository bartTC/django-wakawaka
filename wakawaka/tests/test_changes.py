from django.urls import reverse

from wakawaka.tests.base import BaseTestCase


class ChangesTestCase(BaseTestCase):
    """
    The Changes view displays the actual diff of two revisons.
    """

    def setUp(self):
        super().setUp()

        # Create one page with two revisions
        self.page = self.create_wikipage("WikiIndex", "First Content", "Second Content")
        self.page_url = reverse("wakawaka_changes", kwargs={"slug": "WikiIndex"})

    def test_no_rev_ids_given(self):
        response = self.client.get(self.page_url)
        self.assertEqual(response.status_code, 400)

    def test_nonexisting_rev_ids_given(self):
        url = f"{self.page_url}?a=3&b=4"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_compare_rev_ids(self):
        url = f"{self.page_url}?a=1&b=2"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_compare_same_rev_ids(self):
        url = f"{self.page_url}?a=1&b=1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
