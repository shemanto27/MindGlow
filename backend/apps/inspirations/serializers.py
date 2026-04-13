from rest_framework import serializers
from .models import FavoriteQuoteModel

class FavoriteQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteQuoteModel
        fields = ['id', 'quote', 'author', 'created_at']
        read_only_fields = ['id', 'created_at']
        ref_name = 'InspirationFavoriteQuote'