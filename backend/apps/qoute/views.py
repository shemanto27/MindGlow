from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from .models import FavoriteQuoteModel
from .serializers import FavoriteQuoteSerializer

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