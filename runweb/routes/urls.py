from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'routes.views.overview', name='routes'),
    url(r'^json/$', 'routes.views.overview', {'as_json': True}),
    url(r'^planner/$', 'routes.views.planner', name='planner'),
    url(r'^planner/(\d+)/$', 'routes.views.planner', name='planner_load'),
)
