from rest_framework import serializers
from .models import ConversationModel, MessageModel


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageModel
        fields = ['id', 'conversation', 'sender', 'content', 'created_at']
        read_only_fields = ['id', 'created_at', 'conversation', 'sender']


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = ConversationModel
        fields = ['id', 'title', 'topic', 'summary', 'created_at', 'updated_at', 'messages']


class ConversationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationModel
        fields = ['id', 'title', 'topic', 'summary', 'created_at', 'updated_at']


class ChatRequestSerializer(serializers.Serializer):
    conversation_id = serializers.IntegerField(required=False, allow_null=True)
    message = serializers.CharField()
