from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^login/$', 'runweb.views.session_login', {'as_json': True}),
    url(r'^routes/$', 'routes.views.overview', {'as_json': True}),
    url(r'^init/$', 'api.views.init'),
)
