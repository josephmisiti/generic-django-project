from django.conf.urls import patterns, include, url
from django.contrib import admin

from .core import views as core_views

admin.autodiscover()

urlpatterns = patterns('',
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

    urlpatterns += [
        url(r'^404$', core_views.error404, name='404'),
        url(r'^403$', core_views.error403, name='403'),
        url(r'^500$', core_views.error500, name='500'),
    ]
