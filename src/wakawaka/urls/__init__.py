from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from wakawaka.views import *

# Wiki slugs must been CamelCase but slashes are fine, if each slug
# is also a CamelCase/OtherSide
WIKI_SLUG = r'(?P<slug>((([A-Z]+[a-z]+){2,})(/([A-Z]+[a-z]+){2,})*))'
WIKI_SLUG = getattr(settings, 'WAKAWAKA_SLUG_REGEX', WIKI_SLUG)

urlpatterns = patterns('',
    url(r'^$', index, name='wakawaka_index'),

    # Revision and Page list
    url(r'^history$', revision_list, name='wakawaka_revision_list'),
    url(r'^index$', page_list, name='wakawaka_page_list'),


    # Revision list for page
    url(r'^%s/history$' % WIKI_SLUG, revisions, name='wakawaka_revision_list'),

    # Changes between two revisions, revision id's come from GET
    url(r'^%s/changes$' % WIKI_SLUG, changes, name='wakawaka_changes'),

    # Edit Form
    url(r'^%s/edit/(?P<rev_id>\d+)$' % WIKI_SLUG, login_required(edit), name='wakawaka_edit'),
    url(r'^%s/edit$' % WIKI_SLUG, login_required(edit), name='wakawaka_edit'),

    # Page
    url(r'^%s/rev(?P<rev_id>\d+)$' % WIKI_SLUG, page, name='wakawaka_page'),
    url(r'^%s$' % WIKI_SLUG, page, name='wakawaka_page'),
)
