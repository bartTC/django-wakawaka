from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path

from . import views

# Wiki slugs must been CamelCase but slashes are fine, if each slug
# is also a CamelCase/OtherSide
WIKI_SLUG = r"((([A-Z]+[a-z]+){2,})(/([A-Z]+[a-z]+){2,})*)"
WIKI_SLUG = getattr(settings, "WAKAWAKA_SLUG_REGEX", WIKI_SLUG)

urlpatterns = [
    path("", views.index, name="wakawaka_index"),
    # Revision and Page list
    path("history/", views.revision_list, name="wakawaka_revision_list"),
    path("index/", views.page_list, name="wakawaka_page_list"),
    # Revision list for page
    re_path(
        rf"^(?P<slug>{WIKI_SLUG})/history/$",
        views.revisions,
        name="wakawaka_revision_list",
    ),
    # Changes between two revisions, revision id's come from GET
    re_path(
        rf"^(?P<slug>{WIKI_SLUG})/changes/$", views.changes, name="wakawaka_changes"
    ),
    # Edit Form
    re_path(
        rf"^(?P<slug>{WIKI_SLUG})/edit/(?P<rev_id>\d+)/$",
        login_required(views.edit),
        name="wakawaka_edit",
    ),
    re_path(
        rf"^(?P<slug>{WIKI_SLUG})/edit/$",
        login_required(views.edit),
        name="wakawaka_edit",
    ),
    # Page
    re_path(
        rf"^(?P<slug>{WIKI_SLUG})/rev(?P<rev_id>\d+)/$",
        views.page,
        name="wakawaka_page",
    ),
    re_path(rf"^(?P<slug>{WIKI_SLUG})/$", views.page, name="wakawaka_page"),
]
