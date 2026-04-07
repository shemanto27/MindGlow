from django.contrib import admin
from .models import LearningModel

@admin.register(LearningModel)
class LearningAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'created_at')
    search_fields = ('user__email', 'topic', 'content')
    list_filter = ('created_at',)