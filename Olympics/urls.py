from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Olympics.views.home', name='home'),
    # url(r'^Olympics/', include('Olympics.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^videos/(?P<videoId>/comments)', 'VideoSite.views.addComment'), 
    url(r'^videos/(?P<videoId>.+)', 'VideoSite.views.watchVideo'),
    url(r'^sport/(?P<sportName>.+)/videos', 'VideoSite.views.videosList'),
    url(r'^sport/(?P<sportName>.+)$', 'VideoSite.views.sport'),
    url(r'^search/(?P<searchTerm>.+)', 'VideoSite.views.search'),
    url(r'^search/', 'VideoSite.views.postSearch'),
    url(r'^login/', 'Accounts.views.login'),
    url(r'^register/', 'Accounts.views.register'),
    url(r'^logout/', 'Accounts.views.logout'),
    url(r'^$', 'VideoSite.views.home', name='home'),
    
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
