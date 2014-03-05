from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^planner/$', 'routes.views.planner', name='planner'),
)
