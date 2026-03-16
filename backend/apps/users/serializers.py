from rest_framework import serializers
from .models import CustomUserModel
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

        attrs['user'] = user
        return attrs

class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ['id', 'email', 'is_superuser']

class CustomJWTSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = LoginUserSerializer()


class CustomUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = [
            'id', 'email', 'full_name', 'profile_picture', 'pronouns', 'age_group',
            'life_situation', 'occupation', 'life_feelings', 'faith',
            'inspiration_sources', 'attention_today', 'is_email_verified', 'is_active'
        ]
        read_only_fields = ['id', 'email', 'is_active', 'is_email_verified']


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUserModel
        fields = ['email', 'password']

    def create(self, validated_data):
        return CustomUserModel.objects.create_user(**validated_data)





class OtpVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6, min_length=6)


class ResendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ProfileCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ['full_name', 'age_group', 'life_situation', 'occupation', 'life_feelings', 'faith', 'inspiration_sources', 'attention_today']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['full_name'] = self.user.full_name
        data['is_active'] = self.user.is_active
        return data
