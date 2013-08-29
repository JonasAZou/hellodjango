from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    url(r'^$',            IndexView.as_view(), name='index'),
    url(r'^register/',    RegisterView.as_view(), name='register'),
    url(r'^login/',       LoginView.as_view(), name='login'),
    url(r'^logout/',      LogoutView.as_view(), name='logout'),
    url(r'^add/',         AddView.as_view(), name='add'),
    url(r'^edit/(\d+)/',  EditView.as_view(), name='edit'),
    url(r'^delete/(\d+)/',DeleteView.as_view(), name='delete'),
)
