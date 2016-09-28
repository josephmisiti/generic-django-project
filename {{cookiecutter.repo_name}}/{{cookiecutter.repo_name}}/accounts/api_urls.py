from django.conf.urls import patterns, include, url

from rest_framework import routers

from . import api_views
from rest_framework.authtoken import views as auth_views

router = routers.DefaultRouter(trailing_slash=True)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api/v1/token', auth_views.obtain_auth_token),                
    
    url(r'login$',
        api_views.LoginView.as_view(),
        name='login-endpoint'),
    
    url(r'logout$',
        api_views.LogoutView.as_view(),
        name='logout-endpoint'),              
)
