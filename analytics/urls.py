from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^map/$', 'analytics.views.location_view', name='location_view')
)
