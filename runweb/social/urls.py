from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^friends/$', 'social.views.friendlist'),
    url(r'^request/$', 'social.views.request_friend'),
    url(r'^remove/(\d+)/$', 'social.views.remove_friend'),
    url(r'^accept/(\d+)/$', 'social.views.accept_request'),
    url(r'^deny/(\d+)/$', 'social.views.deny_request'),
)