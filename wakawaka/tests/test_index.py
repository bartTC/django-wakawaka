from django.urls import reverse

from wakawaka.tests.base import BaseTestCase


class IndexTestCase(BaseTestCase):
    """
    Index and WikiIndex tests.
    """

    def test_calling_home_redircts_to_wikiindex(self):
        """
        Calling the homepage `/` will automatically redirect to the
        `WikiIndex` index page.
        """
        response = self.client.get(reverse("wakawaka_index"))
        self.assertEqual(response.status_code, 302)

        if self.is_django_18():
            self.assertEqual(response["Location"], "http://testserver/WikiIndex/")
        else:
            self.assertEqual(response["Location"], "/WikiIndex/")

    def test_wikiindex_is_a_setting(self):
        """
        This Homepage name `WikiIndex` can be set by a setting.
        """
        with self.settings(WAKAWAKA_DEFAULT_INDEX="WikiWukuIndex"):
            response = self.client.get(reverse("wakawaka_index"))
            self.assertEqual(response.status_code, 302)

            if self.is_django_18():
                self.assertEqual(
                    response["Location"],
                    "http://testserver/WikiWukuIndex/",
                )
            else:
                self.assertEqual(response["Location"], "/WikiWukuIndex/")
