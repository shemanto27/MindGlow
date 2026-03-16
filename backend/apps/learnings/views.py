from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from .models import LearningModel
from .serializers import LearningSerializer, LearningRequestSerializer
from ai.chatbot_learning import generate_learning_content

class LearningView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=LearningRequestSerializer,
        responses={201: LearningSerializer},
        security=[{"Bearer": []}]
    )
    def post(self, request):
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
        }

        ai_response = generate_learning_content(user_message=topic, user_metadata=profile_payload)
        content = ai_response.get('reply')

        learning_item = LearningModel.objects.create(
            user=user,
            topic=topic,
            content=content
        )

        output_serializer = LearningSerializer(learning_item)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={200: LearningSerializer(many=True)},
        security=[{"Bearer": []}]
    )
    def get(self, request):
        user = request.user
        learnings = LearningModel.objects.filter(user=user).order_by('-created_at')
        serializer = LearningSerializer(learnings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)