from django.conf.urls import patterns, include, url
from django.contrib import admin

from {{cookiecutter.repo_name}}.core.views import index_view

urlpatterns = patterns('',
    url(r'^$', index_view, name='index'),
    url(r'', include('{{cookiecutter.repo_name}}.core.urls',  namespace='api')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),
    )
