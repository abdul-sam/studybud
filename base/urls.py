from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^login/$', views.login_page, name='login'),
    re_path(r'^register/$', views.register_user, name='register'),
    re_path(r'^logout/$', views.logout_user, name='logout'),
    re_path(r'^room/(?P<pk>\d+)/$', views.room, name='room'),
    re_path(r'^rooms/new/$', views.new_room, name='new_room'),
    re_path(r'^rooms/(?P<pk>\d+)/edit$', views.update_room, name='edit_room'),
    re_path(r'^rooms/(?P<pk>\d+)/delete$', views.delete_room, name='delete_room'),
    re_path(r'^delete_message/(?P<pk>\d+)/$', views.delete_message, name='delete_message'),
]