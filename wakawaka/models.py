from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _


class WikiPage(models.Model):
    slug = models.CharField(_("slug"), max_length=255)
    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(_("modified"), auto_now=True)

    class Meta:
        verbose_name = _("Wiki page")
        verbose_name_plural = _("Wiki pages")
        ordering = ("slug",)

    def __str__(self) -> str:
        return self.slug

    @property
    def current(self) -> WikiPage:
        return self.revisions.latest()


class Revision(models.Model):
    page = models.ForeignKey(
        WikiPage,
        related_name="revisions",
        on_delete=models.CASCADE,
    )
    content = models.TextField(_("content"))
    message = models.TextField(_("change message"), blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="wakawaka_revisions",
        on_delete=models.CASCADE,
    )
    creator_ip = models.GenericIPAddressField(_("creator ip"), blank=True, null=True)
    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(_("modified"), auto_now=True)

    class Meta:
        verbose_name = _("Revision")
        verbose_name_plural = _("Revisions")
        ordering = ("-modified",)
        get_latest_by = "modified"

    def __str__(self) -> str:
        return gettext("Revision %(created)s for %(page_slug)s") % {
            "created": self.created.strftime("%Y%m%d-%H%M"),
            "page_slug": self.page.slug,
        }
