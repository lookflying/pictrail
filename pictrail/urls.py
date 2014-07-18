from django.conf.urls import patterns, url

from pictrail import views

urlpatterns = patterns('',
		url(r'^$', views.interface, name='interface'),
)
