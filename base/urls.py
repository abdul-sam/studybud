from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^login/$', views.login_page, name='login'),
    re_path(r'^register/$', views.register_user, name='register'),
    re_path(r'^logout/$', views.logout_user, name='logout'),
    re_path(r'^profile/(?P<pk>\d+)/$', views.user_profile, name='profile'),
    re_path(r'^update_profile/$', views.update_profile, name='update_profile'),
    re_path(r'^room/(?P<pk>\d+)/$', views.room, name='room'),
    re_path(r'^rooms/new/$', views.new_room, name='new_room'),
    re_path(r'^rooms/(?P<pk>\d+)/edit$', views.update_room, name='edit_room'),
    re_path(r'^rooms/(?P<pk>\d+)/delete$', views.delete_room, name='delete_room'),
    re_path(r'^delete_message/(?P<pk>\d+)/$', views.delete_message, name='delete_message'),
    re_path(r'^topics/$', views.topic_list, name='topics'),
    re_path(r'^activity/$', views.activity_list, name='activity'),
]