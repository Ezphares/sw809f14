from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'routes.views.list', name='routes'),
    url(r'^planner/$', 'routes.views.planner', name='planner'),
    url(r'^planner/(\d+)/$', 'routes.views.planner', name='planner_load'),
)
