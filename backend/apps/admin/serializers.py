from rest_framework import serializers
from .models import FAQModel, PrivacyPolicyModel, TermsAndConditionsModel, SupportMessageModel

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQModel
        fields = '__all__'

class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicyModel
        fields = '__all__'

class TermsAndConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndConditionsModel
        fields = '__all__'

class SupportMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportMessageModel
        fields = '__all__'
        read_only_fields = ['id', 'created_at']