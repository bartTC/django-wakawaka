from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),

    url('^accounts/login/$', auth_views.LoginView.as_view(), name='auth_login'),
    url('^accounts/logout/$', auth_views.LogoutView.as_view(), name='auth_logout'),

    # Include the wacky wakawaka urls
    url(r'^', include('wakawaka.urls')),

    # If all pages are only for authenticated users, import this urlconf instead
    #(r'^', include('wakawaka.urls.authenticated')),
]

urlpatterns += staticfiles_urlpatterns()
