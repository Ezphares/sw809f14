from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^(?:login/)?$', 'runweb.views.session_login', name='login'),
    url(r'^register/$', 'runweb.views.register', name='register'),
    url(r'^logout/$', 'runweb.views.session_logout', name='logout'),
    url(r'^routes/', include('routes.urls')),
    url(r'^social/', include('social.urls')),
    url(r'^api/', include('api.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
