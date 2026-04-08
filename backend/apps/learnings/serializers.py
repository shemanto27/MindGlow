from rest_framework import serializers
from .models import LearningModel

class LearningSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningModel
        fields = ['id', 'topic', 'content', 'created_at']
        read_only_fields = ['id', 'content', 'created_at']

class LearningRequestSerializer(serializers.Serializer):
    topic = serializers.CharField(required=True)

class PastActivitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    date = serializers.SerializerMethodField()
    title = serializers.CharField()
    summary = serializers.CharField()

    def get_date(self, obj):
        # Support both model objects and dictionaries
        created_at = obj.get('created_at') if isinstance(obj, dict) else getattr(obj, 'created_at', None)
        if created_at:
            return created_at.strftime('%B %d')
        return ""