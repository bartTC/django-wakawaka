from __future__ import annotations

import difflib
from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseRedirect,
)
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from wakawaka.forms import DeleteWikiPageForm, WikiPageForm
from wakawaka.models import Revision, WikiPage

if TYPE_CHECKING:
    from django.forms import BaseForm


def index(request: HttpRequest) -> HttpResponseRedirect:
    """
    Redirects to the default wiki index name.
    """
    kwargs = {"slug": getattr(settings, "WAKAWAKA_DEFAULT_INDEX", "WikiIndex")}
    redirect_to = reverse("wakawaka_page", kwargs=kwargs)
    return HttpResponseRedirect(redirect_to)


def page(
    request: HttpRequest,
    slug: str,
    rev_id: int | None = None,
    template_name: str = "wakawaka/page.html",
    extra_context: dict | None = None,
) -> HttpResponse:
    """
    Displays a wiki page. Redirects to the edit view if the page doesn't exist.
    """
    try:
        queryset = WikiPage.objects.all()
        page = queryset.get(slug=slug)
        rev = page.current

        # Display an older revision if rev_id is given
        if rev_id:
            revision_queryset = Revision.objects.all()
            rev_specific = revision_queryset.get(pk=rev_id)
            if rev.pk != rev_specific.pk:
                rev_specific.is_not_current = True
            rev = rev_specific

    # The Page does not exist, redirect to the edit form or
    # deny, if the user has no permission to add pages
    except WikiPage.DoesNotExist as e:
        if request.user.is_authenticated:
            kwargs = {"slug": slug}
            redirect_to = reverse("wakawaka_edit", kwargs=kwargs)
            return HttpResponseRedirect(redirect_to)
        raise Http404 from e
    template_context = {"page": page, "rev": rev}
    template_context.update(extra_context or {})
    return render(request, template_name, template_context)


def edit(  # noqa: C901 PLR0912 PLR0913 - Too complex, too many arguments, too many branches
    request: HttpRequest,
    slug: str,
    rev_id: int | None = None,
    template_name: str = "wakawaka/edit.html",
    extra_context: dict | None = None,
    wiki_page_form: BaseForm = WikiPageForm,
    wiki_delete_form: BaseForm = DeleteWikiPageForm,
) -> HttpResponse:
    """
    Displays the form for editing and deleting a page.
    """
    # Get the page for slug and get a specific revision, if given
    try:
        queryset = WikiPage.objects.all()
        page_obj = queryset.get(slug=slug)
        rev = page_obj.current
        initial = {"content": page_obj.current.content}

        # Do not allow editing wiki pages if the user has no permission
        if not request.user.has_perms(
            ("wakawaka.change_wikipage", "wakawaka.change_revision"),
        ):
            return HttpResponseForbidden(
                gettext("You don't have permission to edit pages."),
            )

        if rev_id:
            # There is a specific revision, fetch this
            rev_specific = Revision.objects.get(pk=rev_id)
            if rev.pk != rev_specific.pk:
                rev = rev_specific
                rev.is_not_current = True
                initial = {
                    "content": rev.content,
                    "message": _('Reverted to "%s"') % rev.message,
                }

    # This page does not exist, create a dummy page
    # Note that it's not saved here
    except WikiPage.DoesNotExist:
        # Do not allow adding wiki pages if the user has no permission
        if not request.user.has_perms(
            ("wakawaka.add_wikipage", "wakawaka.add_revision"),
        ):
            return HttpResponseForbidden(
                gettext("You don't have permission to add wiki pages."),
            )

        page_obj = WikiPage(slug=slug)
        page_obj.is_initial = True
        rev = None
        initial = {
            "content": _("Describe your new page %s here...") % slug,
            "message": _("Initial revision"),
        }

    # Don't display the delete form if the user has nor permission
    delete_form = None
    # The user has permission, then do
    if request.user.has_perm("wakawaka.delete_wikipage") or request.user.has_perm(
        "wakawaka.delete_revision",
    ):
        delete_form = wiki_delete_form(request)
        if request.method == "POST" and request.POST.get("delete"):
            delete_form = wiki_delete_form(request, data=request.POST)
            if delete_form.is_valid():
                return delete_form.delete_wiki(request, page_obj, rev)

    # Page add/edit form
    form = wiki_page_form(initial=initial)
    if request.method == "POST":
        form = wiki_page_form(data=request.POST)
        if form.is_valid():
            # Check if the content is changed, except there is a rev_id and the
            # user possibly only reverted the HEAD to it
            if not rev_id and initial["content"] == form.cleaned_data["content"]:
                form.errors["content"] = (_("You have made no changes!"),)

            # Save the form and redirect to the page view
            else:
                try:
                    # Check that the page already exist
                    queryset = WikiPage.objects.all()
                    page_obj = queryset.get(slug=slug)
                except WikiPage.DoesNotExist:
                    # Must be a new one, create that page
                    page_obj = WikiPage(slug=slug)
                    page_obj.save()

                form.save(request, page_obj)

                kwargs = {"slug": page_obj.slug}

                redirect_to = reverse("wakawaka_page", kwargs=kwargs)
                messages.success(
                    request,
                    gettext("Your changes to %s were saved") % page_obj.slug,
                )
                return HttpResponseRedirect(redirect_to)

    template_context = {
        "form": form,
        "delete_form": delete_form,
        "page": page_obj,
        "rev": rev,
    }
    template_context.update(extra_context or {})
    return render(request, template_name, template_context)


def revisions(
    request: HttpRequest,
    slug: str,
    template_name: str = "wakawaka/revisions.html",
    extra_context: dict | None = None,
) -> HttpResponse:
    """
    Displays the list of all revisions for a specific WikiPage
    """
    queryset = WikiPage.objects.all()
    page = get_object_or_404(queryset, slug=slug)

    template_context = {"page": page}
    template_context.update(extra_context or {})
    return render(request, template_name, template_context)


def changes(
    request: HttpRequest,
    slug: str,
    template_name: str = "wakawaka/changes.html",
    extra_context: dict | None = None,
) -> HttpResponse:
    """
    Displays the changes between two revisions.
    """
    rev_a_id = request.GET.get("a", None)
    rev_b_id = request.GET.get("b", None)

    # Some stinky fingers manipulated the url
    if not rev_a_id or not rev_b_id:
        return HttpResponseBadRequest("Bad Request")

    try:
        revision_queryset = Revision.objects.all()
        wikipage_queryset = WikiPage.objects.all()
        rev_a = revision_queryset.get(pk=rev_a_id)
        rev_b = revision_queryset.get(pk=rev_b_id)
        page = wikipage_queryset.get(slug=slug)
    except ObjectDoesNotExist as e:
        raise Http404 from e

    if rev_a.content != rev_b.content:
        d = difflib.unified_diff(
            rev_b.content.splitlines(),
            rev_a.content.splitlines(),
            "Original",
            "Current",
            lineterm="",
        )
        difftext = "\n".join(d)
    else:
        difftext = _("No changes were made between this two files.")

    template_context = {
        "page": page,
        "diff": difftext,
        "rev_a": rev_a,
        "rev_b": rev_b,
    }
    template_context.update(extra_context or {})
    return render(request, template_name, template_context)


# Some useful views
def revision_list(
    request: HttpRequest,
    template_name: str = "wakawaka/revision_list.html",
    extra_context: dict | None = None,
) -> HttpResponse:
    """
    Displays a list of all recent revisions.
    """
    revisions = Revision.objects.all()
    template_context = {"revision_list": revisions}
    template_context.update(extra_context or {})
    return render(request, template_name, template_context)


def page_list(
    request: HttpRequest,
    template_name: str = "wakawaka/page_list.html",
    extra_context: dict | None = None,
) -> HttpResponse:
    """
    Displays all Pages
    """
    pages = WikiPage.objects.order_by("slug")

    template_context = {
        "page_list": pages,
        "index_slug": getattr(settings, "WAKAWAKA_DEFAULT_INDEX", "WikiIndex"),
    }
    template_context.update(extra_context or {})
    return render(request, template_name, template_context)
