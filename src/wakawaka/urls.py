from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('wakawaka.views',
    url(r'^$', 'index', name='wakawaka_index'),

    # Revision and Page list
    url(r'^history$', 'revision_list', name='wakawaka_revision_list'),
    url(r'^index$', 'page_list', name='wakawaka_page_list'),


    # Revision list for page
    url(r'^(?P<slug>[\w\-/]+)/history$', 'revisions', name='wakawaka_revision_list'),

    # Changes between two revisions, revision id's come from GET
    url(r'^(?P<slug>[\w\-/]+)/changes$', 'changes', name='wakawaka_changes'),

    # Edit Form
    url(r'^(?P<slug>[\w\-/]+)/edit/(?P<rev_id>\d+)$', 'edit', name='wakawaka_edit'),
    url(r'^(?P<slug>[\w\-/]+)/edit$', 'edit', name='wakawaka_edit'),

    # Page
    url(r'^(?P<slug>[\w\-/]+)/rev(?P<rev_id>\d+)', 'page', name='wakawaka_page'),
    url(r'^(?P<slug>[\w\-/]+)', 'page', name='wakawaka_page'),
)
