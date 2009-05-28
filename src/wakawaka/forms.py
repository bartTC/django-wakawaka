from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext
from wakawaka.models import Revision
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from curses.ascii import DEL

class WikiPageForm(forms.Form):
    content = forms.CharField(label=_('Content'), widget=forms.Textarea(attrs={'rows': 30}))
    message = forms.CharField(label=_('Change message (optional)'), widget=forms.TextInput, required=False)

    def save(self, request, page, *args, **kwargs):
        Revision.objects.create(
            page=page,
            creator=request.user,
            creator_ip=request.META['REMOTE_ADDR'],
            content = self.cleaned_data['content'],
            message = self.cleaned_data['message']
        )

DELETE_CHOICES = (

)

class DeleteWikiPageForm(forms.Form):
    delete = forms.ChoiceField(choices=())

    def __init__(self, request, *args, **kwargs):
        '''
        Override the __init__ to display only delete choices the user has
        permission for.
        '''
        self.base_fields['delete'].choices = []
        if request.user.has_perm('wakawaka.delete_revision'):
            self.base_fields['delete'].choices.append(('rev', 'Delete this revision'),)

        if request.user.has_perm('wakawaka.delete_revision') and \
           request.user.has_perm('wakawaka.delete_wikipage'):
            self.base_fields['delete'].choices.append(('page', 'Delete the page with all revisions'),)

        super(DeleteWikiPageForm, self).__init__(*args, **kwargs)

    def _delete_page(self, page):
        page.delete()

    def _delete_revision(self, page, rev):
        # Delete the page if this is the only revision
        if len(page.revisions.all()) <= 1:
            self.delete_page(page)
            return True
        rev.delete()

    def delete_wiki(self, request, page, rev):
        """
        Deletes the page with all revisions or the revision, based on the
        users choice.

        Returns a HttpResponseRedirect.
        """
        # Delete revision
        if self.cleaned_data.get('delete') == 'rev' and \
           request.user.has_perm('wakawaka.delete_revision'):

            page_deleted = self._delete_revision(page, rev)
            if page_deleted:
                # This was the only one revision so the whole page was deleted.
                request.user.message_set.create(message=ugettext('The page for %s was deleted because you deleted the only revision' % page.slug))
                return HttpResponseRedirect(reverse('wakawaka_index'))
            request.user.message_set.create(message=ugettext('The revision for %s was deleted' % page.slug))
            return HttpResponseRedirect(reverse('wakawaka_page', kwargs={'slug': page.slug}))

        # Delete the page
        if self.cleaned_data.get('delete') == 'page' and \
           request.user.has_perm('wakawaka.delete_revision') and \
           request.user.has_perm('wakawaka.delete_wikipage'):

            self._delete_page(page)
            request.user.message_set.create(message=ugettext('The page %s was deleted' % page.slug))
            return HttpResponseRedirect(reverse('wakawaka_index'))
