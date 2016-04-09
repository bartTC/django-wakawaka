from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User


class WikiPage(models.Model):
    slug = models.CharField(_('slug'), max_length=255)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        verbose_name = _("Wiki page")
        verbose_name_plural = _("Wiki pages")
        ordering = ['slug']

    def __unicode__(self):
        return self.slug

    @property
    def current(self):
        return self.revisions.latest()

    @property
    def rev(self, rev_id):
        return self.revisions.get(pk=rev_id)

class Revision(models.Model):
    page = models.ForeignKey(WikiPage, related_name='revisions')
    content = models.TextField(_('content'))
    message = models.TextField(_('change message'), blank=True)
    creator = models.ForeignKey(User, blank=True, null=True, related_name='wakawaka_revisions')
    creator_ip = models.GenericIPAddressField(_('creator ip'))
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        verbose_name = _("Revision")
        verbose_name_plural = _("Revisions")
        ordering = ['-modified']
        get_latest_by = 'modified'

    def __unicode__(self):
        return ugettext('Revision %(created)s for %(page_slug)s') % {
            'created': self.created.strftime('%Y%m%d-%H%M'),
            'page_slug': self.page.slug,
        }

