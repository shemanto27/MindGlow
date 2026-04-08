import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from ..models import CustomUserModel
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers

# Serializers for the flow
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=8)
    confirm_password = serializers.CharField(min_length=8)

class PasswordResetRequestView(APIView):
    """
    Step 1: Request an OTP for password reset.
    """
    @swagger_auto_schema(request_body=PasswordResetRequestSerializer)
    def post(self, request):
        email = request.data.get('email')
        try:
            user = CustomUserModel.objects.get(email=email)
            otp = str(random.randint(100000, 999999))
            user.verification_code = otp
            user.save()

            send_mail(
                subject="Password Reset OTP",
                message=f"Your password reset code is: {otp}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return Response({"detail": "OTP sent to email."}, status=status.HTTP_200_OK)
        except CustomUserModel.DoesNotExist:
            # We return 200 even if user doesn't exist for security (prevent email harvesting)
            return Response({"detail": "If an account exists, an OTP has been sent."}, status=status.HTTP_200_OK)

class PasswordResetVerifyView(APIView):
    """
    Step 2: Verify the OTP matches.
    """
    @swagger_auto_schema(request_body=PasswordResetVerifySerializer)
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        try:
            user = CustomUserModel.objects.get(email=email, verification_code=code)
            return Response({"detail": "OTP verified successfully. You can now reset your password."}, status=status.HTTP_200_OK)
        except CustomUserModel.DoesNotExist:
            return Response({"detail": "Invalid OTP or email."}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    """
    Step 3: Finalize the password reset using the verified OTP.
    """
    @swagger_auto_schema(request_body=PasswordResetConfirmSerializer)
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if new_password != confirm_password:
            return Response({"detail": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUserModel.objects.get(email=email, verification_code=code)
            user.set_password(new_password)
            user.verification_code = None  # Clear OTP after use
            user.save()
            return Response({"detail": "Password reset successful."}, status=status.HTTP_200_OK)
        except CustomUserModel.DoesNotExist:
            return Response({"detail": "Invalid session or OTP."}, status=status.HTTP_400_BAD_REQUEST)
