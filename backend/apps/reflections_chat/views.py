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
                "language": getattr(user, 'language', 'en'),
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




from apps.learnings.serializers import PastActivitySerializer
from rest_framework import generics

class PastReflectionListView(generics.ListAPIView):
    """
    Returns a list of past reflections with special formatting (Date, Title, Summary).
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PastActivitySerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return ConversationModel.objects.none()
        return ConversationModel.objects.filter(user=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = []
        for item in queryset:
            data.append({
                "id": item.id,
                "created_at": item.created_at,
                "title": item.title or "Self Reflection",
                "summary": item.summary or "A moment of reflection."
            })
        
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)

class ReflectedTopicsView(APIView):
    """
    Returns a list of unique topics (single words) the user has reflected on.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: 'List of unique topics the user has reflected on'},
        security=[{"Bearer": []}]
    )
    def get(self, request):
        topics = ConversationModel.objects.filter(
            user=request.user, 
            topic__isnull=False
        ).exclude(topic='').values_list('topic', flat=True).distinct()
        
        cleaned_topics = set()
        for t in topics:
            # Basic heuristic: take the last word and strip punctuation 
            # to handle existing multi-word topics in the database.
            word = t.strip(' .?!,').split()[-1].capitalize()
            cleaned_topics.add(word)
            
        return Response(sorted(list(cleaned_topics)), status=status.HTTP_200_OK)


class LastConversationView(APIView):
    """
    Returns the ID of the most recently updated conversation for the user.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: 'The ID of the most recent conversation'},
        security=[{"Bearer": []}]
    )
    def get(self, request):
        last_convo = ConversationModel.objects.filter(user=request.user).order_by('-updated_at').first()
        return Response({
            "conversation_id": last_convo.id if last_convo else None
        }, status=status.HTTP_200_OK)
