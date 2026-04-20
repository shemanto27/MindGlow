from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .models import LearningModel
from .serializers import LearningSerializer, LearningRequestSerializer, PastActivitySerializer
from ai.chatbot_learning import generate_learning_content

class LearningViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing learning records.
    """
    queryset = LearningModel.objects.all()
    serializer_class = LearningSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return self.queryset.none()
        return self.queryset.filter(user=self.request.user).order_by('-created_at')

    @swagger_auto_schema(
        request_body=LearningRequestSerializer,
        responses={201: LearningSerializer},
        security=[{"Bearer": []}]
    )
    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = LearningRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        topic = serializer.validated_data['topic']

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

        ai_response = generate_learning_content(user_message=topic, user_metadata=profile_payload)
        content = ai_response.get('reply', 'No content generated.')

        learning_item = LearningModel.objects.create(
            user=user,
            topic=topic,
            content=content
        )

        output_serializer = LearningSerializer(learning_item)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class PastLearningListView(generics.ListAPIView):
    """
    Returns a list of past learnings with special formatting (Date, Title, Summary).
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PastActivitySerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return LearningModel.objects.none()
        return LearningModel.objects.filter(user=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = []
        for item in queryset:
            summary_lines = (item.content or "").split('\n')
            summary = "\n".join(summary_lines[:2])
            data.append({
                "id": item.id,
                "created_at": item.created_at,
                "title": item.topic,
                "summary": summary
            })
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)