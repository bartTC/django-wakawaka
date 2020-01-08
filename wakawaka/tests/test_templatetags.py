from __future__ import unicode_literals

from wakawaka.templatetags.wakawaka_tags import wikify
from wakawaka.tests.base import BaseTestCase


class TemplateTagTestCase(BaseTestCase):
    """
    Page names are automatically linked using the `wikify`
    templatetag.

    A valid page name consists of a CamelCase word, and may
    have one or more CamelCase words in them, separated by a
    slash. So these words care valid:

        CarrotCake
        CaCa
        CarrotCake/WithButter
        CarrotCake/WithButter/AndOnions

    But not:

        Carrotcake
        Caca
        Carrotcake/Withbutter
        CarrotCake/Withbutter
        CarrotCake|WithButter
    """

    def test_valid_wikiname_single(self):
        self.create_wikipage('WikiIndex')
        f = wikify('Check WikiIndex out!')
        self.assertEqual(f, 'Check <a href="/WikiIndex/">WikiIndex</a> out!')

    def test_valid_wikiname_slashed(self):
        self.create_wikipage('CarrotCake/WithButter')
        f = wikify('Check CarrotCake/WithButter out!')
        self.assertEqual(
            f, 'Check <a href="/CarrotCake/WithButter/">CarrotCake/WithButter</a> out!',
        )

    def test_invalid_wikiname_single(self):
        f = wikify('Check Carrotcake out!')
        self.assertEqual(f, 'Check Carrotcake out!')

    def test_invalid_wikiname_slashed(self):
        f = wikify('Check Carrotcake/Withbutter out!')
        self.assertEqual(f, 'Check Carrotcake/Withbutter out!')

    def test_valid_wikiname_no_page(self):
        """
        If a Page does not exist, the link is generated nonetheless, going
        to the edit page , so the user can go there, and create the page.
        Those links have a HTML class `doesnotexist` attached.
        """
        f = wikify('Check WikiIndex out!')
        self.assertEqual(
            f,
            'Check <a class="doesnotexist" href="/WikiIndex/edit/">WikiIndex</a> out!',
        )

    def __defunctest_custom_wikiword_regex(self):
        """
        This test does not work, because the urlpattern is generated
        before self.settings() takes places and overwrites it. I leave
        it in for documentation purpose.

        The CamelCase syntax is not fixed and can be easily replaced
        by the WAKAWAKA_SLUG_REGEX setting.
        """
        # All pages must start with "AWESOME" and no slash is allowed
        # followed by an uppercase word.
        custom_slug = r'AWESOME[A-Z][a-z]+)'
        with self.settings(WAKAWAKA_SLUG_REGEX=custom_slug):

            # Page exists
            self.create_wikipage('AWESOMEWiki')
            f = wikify('Check AWESOMEWiki out!')
            self.assertEqual(f, 'Check <a href="/AWESOMEWiki/">AWESOMEWiki</a> out!')

            # Valid slug, but page does not exist
            f = wikify('Check AWESOMEBeansoup out!')
            self.assertEqual(
                f,
                'Check <a class="doesnotexist" href="/AWESOMEBeansoup/edit/">AwesomeBeans</a> out!',
            )
