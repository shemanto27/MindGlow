from django.contrib import admin
from .models import FAQModel, PrivacyPolicyModel, TermsAndConditionsModel, SupportMessageModel

@admin.register(FAQModel)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['id', 'updated_at']

@admin.register(PrivacyPolicyModel)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ['id', 'updated_at']

@admin.register(TermsAndConditionsModel)
class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'updated_at']

@admin.register(SupportMessageModel)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'email', 'created_at']
    readonly_fields = ['subject', 'email', 'message', 'created_at']