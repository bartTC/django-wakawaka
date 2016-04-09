# from http://open.e-scribe.com/browser/python/django/apps/protowiki/templatetags/wikitags.py
# copyright Paul Bissex, MIT license
import re
from django.core.exceptions import ObjectDoesNotExist
from django.template import Library, Node, Variable
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from wakawaka.models import WikiPage
from wakawaka.urls import WIKI_SLUG

register = Library()

WIKI_WORDS_REGEX = re.compile(r'\b%s\b' % WIKI_SLUG, re.UNICODE)


def replace_wikiwords(value):
    def replace_wikiword(m):
        slug = m.group(1)
        try:
            page = WikiPage.objects.get(slug=slug)
            kwargs = {
                'slug': slug,
            }
            url = reverse('wakawaka_page', kwargs=kwargs)
            return r'<a href="%s">%s</a>' % (url, slug)
        except ObjectDoesNotExist:
            kwargs = {
                'slug': slug,
            }
            url = reverse('wakawaka_edit', kwargs=kwargs)
            return r'<a class="doesnotexist" href="%s">%s</a>' % (url, slug)
    return mark_safe(WIKI_WORDS_REGEX.sub(replace_wikiword, value))


@register.filter
def wikify(value):
    """Makes WikiWords"""
    return replace_wikiwords(value)


class WikifyContentNode(Node):
    def __init__(self, content_expr):
        self.content_expr = content_expr

    def render(self, context):
        content = self.content_expr.resolve(context)
        return replace_wikiwords(content)

@register.tag
def wikify_content(parser, token):
    bits = token.split_contents()
    return WikifyContentNode(parser.compile_filter(bits[1]))
