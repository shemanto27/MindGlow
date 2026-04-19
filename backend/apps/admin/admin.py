from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import FAQModel, PrivacyPolicyModel, TermsAndConditionsModel, SupportMessageModel

@admin.register(FAQModel)
class FAQAdmin(ModelAdmin):
    list_display = ('question', 'updated_at')
    search_fields = ('question', 'answer')

@admin.register(PrivacyPolicyModel)
class PrivacyPolicyAdmin(ModelAdmin):
    list_display = ('id', 'updated_at')

@admin.register(TermsAndConditionsModel)
class TermsAndConditionsAdmin(ModelAdmin):
    list_display = ('id', 'updated_at')

@admin.register(SupportMessageModel)
class SupportMessageAdmin(ModelAdmin):
    list_display = ('subject', 'email', 'created_at')
    search_fields = ('subject', 'email', 'message')
    
    def has_add_permission(self, request):
        """Users send support messages; admins only read them."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Prevent admin from editing user support messages."""
        return False

    def get_readonly_fields(self, request, obj=None):
        """All fields should be read-only for support messages."""
        return [f.name for f in self.model._meta.fields]