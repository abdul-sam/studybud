from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^login/$', views.login_page, name='login'),
    re_path(r'^room/(?P<pk>\d+)/$', views.room, name='room'),
    re_path(r'^rooms/new/$', views.new_room, name='new_room'),
    re_path(r'^rooms/(?P<pk>\d+)/edit$', views.update_room, name='edit_room'),
    re_path(r'^rooms/(?P<pk>\d+)/delete$', views.delete_room, name='delete_room'),
]