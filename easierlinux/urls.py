from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Examples:
    url(r'^$', 'easierlinux.views.home', name='home'),
    # url(r'^easierlinux/', include('easierlinux.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #(r'^static/(?P<path>.*)$', 'django.views.static.serve',
    #    {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
    url(r'internet_status/$', 'easierlinux.views.get_internet_status'),
    url(r'set_status/step/(?P<step>[\w\d]*)/running_status/(?P<running_status>[\w\d]*)/$', 'easierlinux.views.set_status'),
    url(r'reset_to_factory_settings_command/$', 'easierlinux.views.reset_to_factory_settings_command'),
    url(r'reset_to_factory_settings/$', 'easierlinux.views.reset_to_factory_settings'),
    url(r'reboot/$', 'easierlinux.views.reboot'),
    url(r'step_2/$', 'easierlinux.views.step_2'),
    url(r'go_to_step/(?P<step>\d+)/$', 'easierlinux.views.go_to_step'),
)

urlpatterns += staticfiles_urlpatterns()
