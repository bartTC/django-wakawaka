import re

from django.core.exceptions import ObjectDoesNotExist
from django.template import Library
from django.urls import reverse
from django.utils.safestring import mark_safe

from wakawaka.models import WikiPage
from wakawaka.urls import WIKI_SLUG

register = Library()

WIKI_WORDS_REGEX = re.compile(r"\b%s\b" % WIKI_SLUG, re.UNICODE)


def replace_wikiwords(value):
    def replace_wikiword(m):
        slug = m.group(1)
        try:
            page = WikiPage.objects.get(slug=slug)
            url = reverse("wakawaka_page", kwargs={"slug": slug})
            return rf'<a href="{url}">{page.slug}</a>'
        except ObjectDoesNotExist:
            url = reverse("wakawaka_edit", kwargs={"slug": slug})
            return rf'<a class="doesnotexist" href="{url}">{slug}</a>'

    return mark_safe(WIKI_WORDS_REGEX.sub(replace_wikiword, value))


@register.filter
def wikify(value):
    """Makes WikiWords"""
    return replace_wikiwords(value)
