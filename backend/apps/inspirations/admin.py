from django.contrib import admin
from .models import FavoriteQuoteModel

@admin.register(FavoriteQuoteModel)
class FavoriteQuoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'author', 'created_at')
    search_fields = ('user__email', 'author', 'quote')
    list_filter = ('created_at',)