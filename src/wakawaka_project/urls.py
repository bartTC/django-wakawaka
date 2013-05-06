from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    url('^accounts/login/$', login, name='auth_login'),
    url('^accounts/logout/$', logout, name='auth_logout'),

    # Include the wacky wakawaka urls
    (r'^', include('wakawaka.urls')),

    # If all pages are only for authenticated users, import this urlconf instead
    #(r'^', include('wakawaka.urls.authenticated')),
)

urlpatterns += staticfiles_urlpatterns()