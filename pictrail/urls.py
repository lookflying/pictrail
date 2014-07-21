from django.conf.urls import patterns, url

from pictrail import views

urlpatterns = patterns('',
		url(r'^$', views.interface, name='interface'),
		url(r'^manage/$', views.manage, name='manage'),

)
