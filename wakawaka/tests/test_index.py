from django.urls import reverse

from wakawaka.tests.base import BaseTestCase


class IndexTestCase(BaseTestCase):
    """
    Index and WikiIndex tests.
    """

    def test_calling_home_redircts_to_wikiindex(self) -> None:
        """
        Calling the homepage `/` will automatically redirect to the
        `WikiIndex` index page.
        """
        response = self.client.get(reverse("wakawaka_index"))
        assert response.status_code == 302
        assert response["Location"] == "/WikiIndex/"

    def test_wikiindex_is_a_setting(self) -> None:
        """
        This Homepage name `WikiIndex` can be set by a setting.
        """
        with self.settings(WAKAWAKA_DEFAULT_INDEX="WikiWukuIndex"):
            response = self.client.get(reverse("wakawaka_index"))
            assert response.status_code == 302
            assert response["Location"] == "/WikiWukuIndex/"
