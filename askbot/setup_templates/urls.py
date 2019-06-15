"""
main url configuration file for the askbot site
"""
from django.conf import settings
try:
    from django.conf.urls import handler404
    from django.conf.urls import include, url
except ImportError:
    from django.conf.urls.defaults import handler404
    from django.conf.urls.defaults import include, url

import askbot
from askbot.views.error import internal_error as handler500
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

if askbot.is_multilingual():
    from django.conf.urls.i18n import i18n_patterns
    urlpatterns = i18n_patterns(
        url(r'%s' % settings.ASKBOT_URL, include('askbot.urls'))
    )
else:
    urlpatterns = [
        url(r'%s' % settings.ASKBOT_URL, include('askbot.urls'))
    ]

urlpatterns += [
    url(r'^admin/', include(admin.site.urls)),
    #(r'^cache/', include('keyedcache.urls')), - broken views disable for now
    #(r'^settings/', include('askbot.deps.livesettings.urls')),
    url(r'^followit/', include('followit.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^robots.txt$', include('robots.urls')),
    url( # TODO: replace with django.conf.urls.static ?
        r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
        django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT.replace('\\','/')},
    )
]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
                    url(r'^rosetta/', include('rosetta.urls')),
                ]

handler500 = 'askbot.views.error.internal_error'
