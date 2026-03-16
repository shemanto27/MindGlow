import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from ..serializers import *
from ..models import CustomUserModel
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema


class SignupView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegistrationSerializer)
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp = str(random.randint(100000, 999999))
            user.verification_code = otp
            user.save()
            # TODO: Add email sending settings properly
            send_mail(
                subject="Verify your Email",
                message=f"Your verification code is: {otp}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
            return Response({"message": "OTP sent to email", "email": user.email}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=OtpVerificationSerializer)
    def post(self, request):
        serializer = OtpVerificationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        try:
            user = CustomUserModel.objects.get(email=email)
        except CustomUserModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if user.verification_code == code:
            user.is_email_verified = True
            user.verification_code = None
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response({"message": "Email verified", "access": str(refresh.access_token), "refresh": str(refresh)}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)


class CompleteProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ProfileCompletionSerializer)
    def post(self, request):
        user = request.user
        
        if not user.is_email_verified:
            return Response({"error": "Verify your email first"}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProfileCompletionSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ResendOTPView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=ResendOtpSerializer)
    def post(self, request):
        serializer = ResendOtpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        try:
            user = CustomUserModel.objects.get(email=email)
        except CustomUserModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        otp = str(random.randint(100000, 999999))
        user.verification_code = otp
        user.save()
        send_mail(
            subject="Verify your Email",
            message=f"Your verification code is: {otp}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
        return Response({"message": "OTP resent"}, status=status.HTTP_200_OK)
