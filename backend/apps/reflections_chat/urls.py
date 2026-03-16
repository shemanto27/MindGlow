from django.urls import path

from apps.reflections_chat.views import ChatView, ConversationDeleteView, ConversationListView, ConversationMessagesView, NewConversationView

urlpatterns = [
    # Add your routes here

    path('chat/conversations/', ConversationListView.as_view(), name='chat-conversations-list'),
    path('chat/conversations/new/', NewConversationView.as_view(), name='chat-new-conversation'),
    path('chat/conversations/<int:pk>/messages/', ConversationMessagesView.as_view(), name='chat-conversation-messages'),
    path('chat/conversations/<int:pk>/delete/', ConversationDeleteView.as_view(), name='chat-conversation-delete'),

    path('chat/', ChatView.as_view(), name='chat'),
]
