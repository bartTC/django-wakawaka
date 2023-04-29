from django.urls import path, re_path
from django.contrib.auth.decorators import login_required

from wakawaka.views import *

# Wiki slugs must been CamelCase but slashes are fine, if each slug
# is also a CamelCase/OtherSide
WIKI_SLUG = r'((([A-Z]+[a-z]+){2,})(/([A-Z]+[a-z]+){2,})*)'
WIKI_SLUG = getattr(settings, 'WAKAWAKA_SLUG_REGEX', WIKI_SLUG)

urlpatterns = [
    path('', index, name='wakawaka_index'),
    # Revision and Page list
    path('history/', revision_list, name='wakawaka_revision_list'),
    path('index/', page_list, name='wakawaka_page_list'),
    # Revision list for page
    re_path(
        r'^(?P<slug>%s)/history/$' % WIKI_SLUG,
        revisions,
        name='wakawaka_revision_list',
    ),
    # Changes between two revisions, revision id's come from GET
    re_path(r'^(?P<slug>%s)/changes/$' % WIKI_SLUG, changes, name='wakawaka_changes'),
    # Edit Form
    re_path(
        r'^(?P<slug>%s)/edit/(?P<rev_id>\d+)/$' % WIKI_SLUG,
        login_required(edit),
        name='wakawaka_edit',
    ),
    re_path(
        r'^(?P<slug>%s)/edit/$' % WIKI_SLUG, login_required(edit), name='wakawaka_edit',
    ),
    # Page
    re_path(r'^(?P<slug>%s)/rev(?P<rev_id>\d+)/$' % WIKI_SLUG, page, name='wakawaka_page',),
    re_path(r'^(?P<slug>%s)/$' % WIKI_SLUG, page, name='wakawaka_page'),
]
