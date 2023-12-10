from django.contrib import admin
from .models import Message, Chat

class ChatAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_display_links = ('id',)
    search_fields = ('id',)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'content')
    list_display_links = ('id', 'content')
    search_fields = ('content',)


admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
