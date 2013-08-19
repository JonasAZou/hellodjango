from django.conf.urls import patterns, include, url
from polls import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
    url(r'^(\d+)/result/$', views.result, name='result'),
    url(r'^(\d+)/vote/$', views.vote, name='vote'),
)
