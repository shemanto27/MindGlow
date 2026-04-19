from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import AIPrompt

@admin.register(AIPrompt)
class AIPromptAdmin(ModelAdmin):
    list_display = ('name', 'description', 'updated_at')
    search_fields = ('name', 'description')
    
    def has_add_permission(self, request):
        """Prevent admin from adding new prompts; prompts should be defined in code/seeding."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Prevent admin from deleting critical system prompts."""
        return False

    def get_readonly_fields(self, request, obj=None):
        """Make name read-only once created, as the AI logic depends on specific names."""
        if obj: # editing an existing object
            return ('name', 'created_at', 'updated_at')
        return ('created_at', 'updated_at')
    
    # Optional: Improve field display in admin
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ('Prompt Content', {
            'fields': ('prompt_text',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )