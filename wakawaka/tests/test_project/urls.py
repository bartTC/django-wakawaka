from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url('^accounts/login/$', auth_views.LoginView.as_view(), name='auth_login'),
    url('^accounts/logout/$', auth_views.LogoutView.as_view(), name='auth_logout'),

    # Include the wakawaka urls
    url(r'^', include('wakawaka.urls')),
]

urlpatterns += staticfiles_urlpatterns()
