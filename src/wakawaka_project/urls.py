from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import login, logout

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
