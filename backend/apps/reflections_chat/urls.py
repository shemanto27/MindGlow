from django.urls import path

from apps.reflections_chat.views import (
    ChatView, ConversationDeleteView, ConversationListView, 
    ConversationMessagesView, NewConversationView, PastReflectionListView,
    ReflectedTopicsView, LastConversationView
)

urlpatterns = [
    # Add your routes here
    path('past-reflection/', PastReflectionListView.as_view(), name='past-reflection'),
    path('topics/', ReflectedTopicsView.as_view(), name='reflected-topics'),
    path('chat/last/', LastConversationView.as_view(), name='last-conversation'),

    path('chat/conversations/', ConversationListView.as_view(), name='chat-conversations-list'),
    path('chat/conversations/new/', NewConversationView.as_view(), name='chat-new-conversation'),
    path('chat/conversations/<int:pk>/messages/', ConversationMessagesView.as_view(), name='chat-conversation-messages'),
    path('chat/conversations/<int:pk>/delete/', ConversationDeleteView.as_view(), name='chat-conversation-delete'),

    path('chat/', ChatView.as_view(), name='chat'),
]
