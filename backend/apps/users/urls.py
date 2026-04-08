from django.urls import path, include

from .views.registration import *
from .views.auth import PasswordResetConfirmHTMLView, ManualPasswordResetConfirmView
from rest_framework_simplejwt.views import TokenRefreshView
from dj_rest_auth.views import PasswordResetConfirmView

from .views.profile import CustomUserDetailsView
from .views.password_reset import PasswordResetRequestView, PasswordResetVerifyView, PasswordResetConfirmView
from .views.stats import UserSummaryView

urlpatterns = [
    # Add your routes here

    # User Summary/Stats
    path('auth/user/summary/', UserSummaryView.as_view(), name='user-summary'),

    # Signup Routes
    path('signup/', SignupView.as_view(), name='signup'),
    path('signup/verify-otp/', VerifyEmailView.as_view(), name='verify-otp'),
    path('signup/complete-profile/', CompleteProfileView.as_view()),
    path('signup/resend-otp/', ResendOTPView.as_view(), name='resend-otp'),

    # Profile Route
    path('auth/user/', CustomUserDetailsView.as_view(), name='rest_user_details'),
    
    # Password Reset via OTP
    path('auth/password/reset/', PasswordResetRequestView.as_view(), name='password_reset_otp_request'),
    path('auth/password/reset/verify/', PasswordResetVerifyView.as_view(), name='password_reset_otp_verify'),
    path('auth/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_otp_confirm'),

    # This adds: login/, logout/, and other standard auth routes
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
