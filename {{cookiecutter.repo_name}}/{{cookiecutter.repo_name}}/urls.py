from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'', include('{{cookiecutter.repo_name}}.core.urls',  namespace='api')),
    url(r'^admin/', include(admin.site.urls)),
)
