from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from django.views.decorators.cache import cache_page

from sbooth.doodle.views import Photos

urlpatterns = patterns('',
    (r'^favicon.ico', RedirectView.as_view(url='static/doodle/favicon.png')),
    
    url(r'^photos/$', cache_page(Photos.as_view(), 1), name="index"),
    url(r'^photos/(\d+)/$', 'sbooth.doodle.views.photo', name='photo'),
    url(r'^$', 'sbooth.doodle.views.home', name='home'),
    
    # url(r'^sbooth/', include('sbooth.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
  urlpatterns += patterns('',
    url(r'^uploads(?P<path>.*)$', 'django.views.static.serve',  {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
  )
