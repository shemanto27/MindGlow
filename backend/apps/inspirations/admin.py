from django.contrib import admin
from .models import FavoriteQuoteModel

@admin.register(FavoriteQuoteModel)
class FavoriteQuoteAdmin(admin.ModelAdmin):
    list_display = ['author', 'user', 'created_at']
    search_fields = ['author', 'quote', 'user__email']