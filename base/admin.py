from django.contrib import admin
from .models import Message, Room, Topic

class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'body', 'updated_at', 'created_at')


class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'updated_at', 'created_at')


class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated_at', 'created_at')


admin.site.register(Message, MessageAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Topic, TopicAdmin)