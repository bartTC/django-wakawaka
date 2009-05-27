from django import forms
from django.utils.translation import ugettext_lazy as _
from wakawaka.models import WikiPage, Revision

class WikiPageForm(forms.Form):
    content = forms.CharField(label=_('Content'), widget=forms.Textarea(attrs={'rows': 30}))
    message = forms.CharField(label=_('Change message (optional)'), widget=forms.TextInput, required=False)

    def save(self, request, page, *args, **kwargs):
        Revision.objects.create(
            page=page,
            creator=request.user,
            creator_ip='127.0.0.1', #FIXME:
            content = self.cleaned_data['content'],
            message = self.cleaned_data['message']
        )

DELETE_CHOICES = (
    ('rev', 'Delete this revision'),
    ('page', 'Delete the page with all revisions'),
)

class DeleteWikiPageForm(forms.Form):
    delete = forms.ChoiceField(choices=DELETE_CHOICES)

    def delete_page(self, page):
        page.delete()

    def delete_revision(self, page, rev):
        # Delete the page if this is the only revision
        if len(page.revisions.all()) <= 1:
            self.delete_page(page)
            return True
        # Or delete this revision only
        rev.delete()