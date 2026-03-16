from rest_framework import serializers
from .models import LearningModel

class LearningSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningModel
        fields = ['id', 'topic', 'content', 'created_at']
        read_only_fields = ['id', 'content', 'created_at']

class LearningRequestSerializer(serializers.Serializer):
    topic = serializers.CharField(required=True)