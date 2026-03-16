from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from ai.youtube_search import YouTubeSearcher
from ai.config import get_settings
from ai.inspire_quote import generate_personalized_quote
from .models import FavoriteQuoteModel
from .serializers import FavoriteQuoteSerializer

class InspirationVideoListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: 'List of YouTube video suggestions'},
        security=[{"Bearer": []}]
    )
    def get(self, request):
        user = request.user
        settings = get_settings()
        
        if not settings.YOUTUBE_API_KEY:
            return Response({"detail": "YouTube API key is not configured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        searcher = YouTubeSearcher(settings.YOUTUBE_API_KEY)
        
        keywords = []
        if user.attention_today and user.attention_today != 'other':
            keywords.append(f"how to handle {user.attention_today} reflection")
        if user.life_feelings:
            keywords.append(f"finding peace with {user.life_feelings} feelings")
        if user.inspiration_sources:
            keywords.append(f"{user.inspiration_sources} wisdom")
        elif user.faith:
            keywords.append(f"{user.faith} spiritual growth")
            
        if not keywords:
            keywords.append("mindfulness reflection for inner peace")
            
        video_results = []
        for kw in keywords[:3]:
            videos = searcher.search_video(kw, max_results=2)
            video_results.extend(videos)
            
        seen_urls = set()
        unique_videos = []
        for v in video_results:
            if v['url'] not in seen_urls:
                unique_videos.append(v)
                seen_urls.add(v['url'])
                
        return Response(unique_videos[:5], status=status.HTTP_200_OK)


class PersonalizedQuoteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: 'A personalized inspiring quote'},
        security=[{"Bearer": []}]
    )
    def get(self, request):
        user = request.user
        profile_payload = {
            "full_name": getattr(user, 'full_name', None),
            "age_group": getattr(user, 'age_group', None),
            "life_situation": getattr(user, 'life_situation', None),
            "life_feelings": getattr(user, 'life_feelings', None),
            "faith": getattr(user, 'faith', None),
            "inspiration_sources": getattr(user, 'inspiration_sources', None),
            "attention_today": getattr(user, 'attention_today', None),
        }
        
        quote_data = generate_personalized_quote(user_metadata=profile_payload)
        return Response(quote_data, status=status.HTTP_200_OK)


class FavoriteQuoteListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: FavoriteQuoteSerializer(many=True)},
        security=[{"Bearer": []}]
    )
    def get(self, request):
        favorites = FavoriteQuoteModel.objects.filter(user=request.user).order_by('-created_at')
        serializer = FavoriteQuoteSerializer(favorites, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=FavoriteQuoteSerializer,
        responses={201: FavoriteQuoteSerializer},
        security=[{"Bearer": []}]
    )
    def post(self, request):
        serializer = FavoriteQuoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FavoriteQuoteDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={204: 'No Content'},
        security=[{"Bearer": []}]
    )
    def delete(self, request, pk):
        quote = get_object_or_404(FavoriteQuoteModel, pk=pk, user=request.user)
        quote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)