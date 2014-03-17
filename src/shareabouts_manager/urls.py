from __future__ import unicode_literals

from django.conf.urls import patterns, url
from shareabouts_manager.views import datasets_view, signup_view, signin_view, password_reset_view, help_view, robots_view, sitemap_view, index_view, profile_view, set_card_info_view

urlpatterns = patterns('',

    url(r'^datasets/$', datasets_view, name='manager-datasets'),
    url(r'^profile/$', profile_view, name='manager-profile'),
    url(r'^profile/set-credit-card$', set_card_info_view, name='manager-set-card-info'),
    url(r'^signup/$', signup_view, name='manager-signup'),
    url(r'^signin/$', signin_view, name='manager-signin'),
    url(r'^signout/$', 'django.contrib.auth.views.logout', name='manager-signout', kwargs={'next_page': '/'}),
    url(r'^password-reset/$', password_reset_view, name='manager-password-reset'),
    url(r'^help/$', help_view, name='manager-help'),
    url(r'^robots.txt$', robots_view, name='manager-robots'),
    url(r'^sitemap.xml$', sitemap_view, name='manager-sitemap'),
    url(r'^$', index_view, name='manager-index'),
)
