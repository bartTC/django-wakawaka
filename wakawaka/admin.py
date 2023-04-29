from django.contrib import admin

from wakawaka.models import Revision, WikiPage


class RevisionInlines(admin.TabularInline):
    model = Revision
    extra = 1


@admin.register(WikiPage)
class WikiPageAdmin(admin.ModelAdmin):
    inlines = [RevisionInlines]


@admin.register(Revision)
class RevisionAdmin(admin.ModelAdmin):
    pass


