from django.urls import include, path, re_path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='auth_login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='auth_logout',),
    # Include the wakawaka urls
    path('', include('wakawaka.urls')),
]

urlpatterns += staticfiles_urlpatterns()
