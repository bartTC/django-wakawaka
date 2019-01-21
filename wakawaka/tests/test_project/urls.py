from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url('^accounts/login/$', auth_views.LoginView.as_view(), name='auth_login'),
    url('^accounts/logout/$', auth_views.LogoutView.as_view(), name='auth_logout'),

    # Include the wakawaka urls
    url(r'^', include('wakawaka.urls')),
]

urlpatterns += staticfiles_urlpatterns()
