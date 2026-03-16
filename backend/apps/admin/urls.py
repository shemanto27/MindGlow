from django.urls import path
from .views import FAQView, PrivacyPolicyView, TermsAndConditionsView, SupportMessageCreateView, SupportMessageListView

urlpatterns = [
    path('faq/', FAQView.as_view(), name='faq'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms-and-conditions/', TermsAndConditionsView.as_view(), name='terms-and-conditions'),
    path('contact-support/', SupportMessageCreateView.as_view(), name='contact-support'),
    path('support-messages/', SupportMessageListView.as_view(), name='support-messages'),
]