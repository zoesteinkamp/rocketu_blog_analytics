from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^blog/$', 'blog.views.blog', name='blog'),
    url(r'^blog/(\d+)/$', 'blog.views.post', name='post'),
    url(r'^blog/(?P<tag_name>\w+)', 'blog.views.filter_by_tags', name='filter_tags'),
    url(r'^email_signup/$', 'blog.views.email_signup', name='email_signup'),
    url(r'^register/$', 'blog.views.register', name='register')
)