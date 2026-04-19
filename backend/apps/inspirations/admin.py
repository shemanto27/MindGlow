from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import FavoriteQuoteModel

@admin.register(FavoriteQuoteModel)
class FavoriteQuoteAdmin(ModelAdmin):
    list_display = ('user', 'author', 'created_at')
    search_fields = ('user__email', 'author', 'quote')
    list_filter = ('created_at',)