from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from .models import ConversationModel, MessageModel
from .serializers import ConversationSerializer, MessageSerializer, ChatRequestSerializer, ConversationListSerializer
from ai.chatbot_reflect import generate_ai_reply


class NewConversationView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={201: ConversationSerializer},
        security=[{"Bearer": []}]
    )
    def post(self, request):
        user = request.user
        conversation = ConversationModel.objects.create(
            user=user,
            title="New reflection"
        )
        serializer = ConversationSerializer(conversation, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ChatRequestSerializer,
        responses={200: ConversationSerializer},
        security=[{"Bearer": []}]
    )
    def post(self, request):
        user = request.user
        if not user or getattr(user, "is_anonymous", False):
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_message = serializer.validated_data['message']
        conversation_id = serializer.validated_data.get('conversation_id')

        with transaction.atomic():
            if conversation_id:
                conversation = get_object_or_404(ConversationModel, id=conversation_id, user=user)
            else:
                conversation = ConversationModel.objects.filter(user=user).order_by('-updated_at').first()

            if not conversation:
                conversation = ConversationModel.objects.create(user=user, title=user_message[:80])

            MessageModel.objects.create(
                conversation=conversation,
                content=user_message,
                sender='user'
            )

            history = [
                {"role": "assistant" if m.sender == 'ai' else "user", "content": m.content}
                for m in conversation.messages.order_by('created_at')
            ]

            profile_payload = {
                "email": user.email,
                "full_name": getattr(user, 'full_name', None),
                "age_group": getattr(user, 'age_group', None),
                "life_situation": getattr(user, 'life_situation', None),
                "occupation": getattr(user, 'occupation', None),
                "life_feelings": getattr(user, 'life_feelings', None),
                "faith": getattr(user, 'faith', None),
                "inspiration_sources": getattr(user, 'inspiration_sources', None),
                "attention_today": getattr(user, 'attention_today', None),
            }

            ai_response = generate_ai_reply(history=history, user_message=user_message, user_metadata=profile_payload)
            
            if isinstance(ai_response, dict):
                reply_text = ai_response.get('reply', '')
                if ai_response.get('crisis_detected') and ai_response.get('crisis_resources'):
                    reply_text += f"\n\n{ai_response['crisis_resources']}"
                
                # Update conversation metadata
                conversation.title = ai_response.get('title', conversation.title)
                conversation.topic = ai_response.get('topic', conversation.topic)
                conversation.summary = ai_response.get('summary', conversation.summary)
                conversation.save()
            else:
                reply_text = str(ai_response)

            MessageModel.objects.create(
                conversation=conversation,
                content=reply_text,
                sender='ai'
            )

        serializer = ConversationSerializer(conversation, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConversationListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: ConversationListSerializer(many=True)},
        security=[{"Bearer": []}]
    )
    def get(self, request):
        user = request.user
        qs = ConversationModel.objects.filter(user=user).order_by('-updated_at')
        data = ConversationListSerializer(qs, many=True, context={'request': request}).data
        return Response(data, status=status.HTTP_200_OK)


class ConversationMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: MessageSerializer(many=True)},
        security=[{"Bearer": []}]
    )
    def get(self, request, pk):
        user = request.user
        conversation = get_object_or_404(ConversationModel, id=pk, user=user)
        msgs = conversation.messages.order_by('created_at')
        data = MessageSerializer(msgs, many=True, context={'request': request}).data
        return Response(data, status=status.HTTP_200_OK)


class ConversationDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={204: 'Deleted', 404: 'Not found'},
        security=[{"Bearer": []}]
    )
    def delete(self, request, pk):
        user = request.user
        conversation = get_object_or_404(ConversationModel, id=pk, user=user)
        conversation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



