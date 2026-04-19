from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import ConversationModel, MessageModel

@admin.register(ConversationModel)
class ConversationAdmin(ModelAdmin):
    list_display = ('id', 'user', 'title', 'topic', 'created_at', 'updated_at')
    search_fields = ('user__email', 'title', 'topic', 'summary')
    list_filter = ('created_at', 'updated_at')

@admin.register(MessageModel)
class MessageAdmin(ModelAdmin):
    list_display = ('id', 'conversation', 'sender', 'created_at')
    search_fields = ('content',)
    list_filter = ('sender', 'created_at')