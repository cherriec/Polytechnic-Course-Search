from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^forum/main/$', views.forumlist, name='forumlist'),
    url(r'^forum/(?P<pk>\d+)/$', views.forumview, name='forumview'),
    url(r'^thread/(?P<pk>\d+)/$', views.threadview, name='threadview'),
    url(r'^post/(?P<pk>\d+)/$', views.postview, name='postview'),
    url(r'^post/(?P<pk>\d+)/new/$', views.replypost, name='replypost'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.editpost, name='editpost'),
    url(r'^thread/(?P<pk>\d+)/new/$', views.addthread, name='addthread'),
    url(r'^delete/(?P<pk>\d+)/$', views.delete_post, name='delete'),
    url(r'^delete_thread/(?P<pk>\d+)/$', views.delete_thread, name='deletethread'),
]