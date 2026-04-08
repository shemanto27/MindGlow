from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.reflections_chat.models import ConversationModel
from apps.learnings.models import LearningModel
from django.db.models.functions import TruncDate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UserSummaryView(APIView):
    """
    Returns a summary of the logged-in user's activity.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: openapi.Response(
            description="User's activity statistics",
            examples={
                "application/json": {
                    "reflections_count": 15,
                    "learnings_count": 8,
                    "active_reflection_days": 10
                }
            }
        )}
    )
    def get(self, request):
        user = request.user

        # 1. Total reflections (Conversations)
        reflections_count = ConversationModel.objects.filter(user=user).count()

        # 2. Total learnings
        learnings_count = LearningModel.objects.filter(user=user).count()

        # 3. How many unique days the user had a reflection
        # We truncate the datetime to date, then count the unique occurrences
        active_days_count = ConversationModel.objects.filter(user=user)\
            .annotate(date=TruncDate('created_at'))\
            .values('date')\
            .distinct()\
            .count()

        return Response({
            "reflections_count": reflections_count,
            "learnings_count": learnings_count,
            "active_reflection_days": active_days_count
        }, status=status.HTTP_200_OK)
