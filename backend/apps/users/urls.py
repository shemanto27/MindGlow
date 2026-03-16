from django.urls import path, include

from .views.registration import *
from .views.auth import PasswordResetConfirmHTMLView, ManualPasswordResetConfirmView
from rest_framework_simplejwt.views import TokenRefreshView
from dj_rest_auth.views import PasswordResetConfirmView

urlpatterns = [
    # Add your routes here

    # Signup Routes
    path('signup/', SignupView.as_view(), name='signup'),
    path('signup/verify-otp/', VerifyEmailView.as_view(), name='verify-otp'),
    path('signup/complete-profile/', CompleteProfileView.as_view()),
    path('signup/resend-otp/', ResendOTPView.as_view(), name='resend-otp'),

    # This adds: password/reset/, password/change/, login/, logout/, and user/
    path('auth/', include('dj_rest_auth.urls')),

    # Required for dj-rest-auth to generate the reset link in the email
    path(
        'auth/password/reset/confirm/<uidb64>/<token>/',
        PasswordResetConfirmHTMLView.as_view(),
        name='password_reset_confirm'
    ),

    # Custom Manual Reset for the HTML page
    path('auth/password/reset/confirm/manual/', ManualPasswordResetConfirmView.as_view(), name='manual-password-reset-confirm'),

    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),    
]
