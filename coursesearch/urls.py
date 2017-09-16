from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.course_search, name='course_search'),

    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^signup/$', views.signup, name='signup'),

    url(r'^profile/view/$', views.profile_view, name='profile_view'),
    url(r'^profile/edit/$', views.profile_edit, name='profile_edit'),
    url(r'^profile/recommend/$', views.profile_recommend, name='profile_recommend'),
    url(r'^profile/add/course_(?P<code>[\w\-]+)/$', views.profile_add_target, name='profile_add_target'),
    url(r'^profile/edit/course/$', views.profile_edit_target, name='profile_edit_target'),
    
    url(r'^keyword-search$', views.keyword_search, name='keyword_search'),
    url(r'^category/(?P<cat>[\w\-]+)/$', views.cat_search, name='cat_search'),
    url(r'^school/(?P<sch>[\w\-]+)/$', views.school_search, name='school_search'),
    
]
