from django.conf.urls import patterns, include, url

from rest_framework import routers
from rest_framework.authtoken import views as auth_views

from . import views

router = routers.DefaultRouter(trailing_slash=True)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    
    # API calls
    url(r'^api/v1/', include('{{cookiecutter.repo_name}}.accounts.api_urls')),
    
)
