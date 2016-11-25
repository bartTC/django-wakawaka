from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.six import python_2_unicode_compatible
from django.utils.translation import ugettext, ugettext_lazy as _


@python_2_unicode_compatible
class WikiPage(models.Model):
    slug = models.CharField(_('slug'), max_length=255)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        verbose_name = _("Wiki page")
        verbose_name_plural = _("Wiki pages")
        ordering = ['slug']

    def __str__(self):
        return self.slug

    @property
    def current(self):
        return self.revisions.latest()

    def rev(self, rev_id):
        return self.revisions.get(pk=rev_id)


@python_2_unicode_compatible
class Revision(models.Model):
    page = models.ForeignKey(WikiPage, related_name='revisions')
    content = models.TextField(_('content'))
    message = models.TextField(_('change message'), blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='wakawaka_revisions')
    creator_ip = models.GenericIPAddressField(_('creator ip'))
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        verbose_name = _("Revision")
        verbose_name_plural = _("Revisions")
        ordering = ['-modified']
        get_latest_by = 'modified'

    def __str__(self):
        return ugettext('Revision %(created)s for %(page_slug)s') % {
            'created': self.created.strftime('%Y%m%d-%H%M'),
            'page_slug': self.page.slug,
        }

