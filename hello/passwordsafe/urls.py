from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^register/', register, name='register'),
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
)
