from django.urls import path, re_path
from . import views

urlpatterns = [
  path('', views.get_routes),
  path('rooms/', views.get_rooms),
  re_path(r'^rooms/(?P<pk>\d+)/$', views.get_room),
]