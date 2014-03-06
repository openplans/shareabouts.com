from django.conf.urls import patterns, include, url
import shareabouts_manager.urls
import sa_api_v2.urls

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v2/', include(sa_api_v2.urls)),
    url(r'^', include(shareabouts_manager.urls)),
)
