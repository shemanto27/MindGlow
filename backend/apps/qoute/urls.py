from django.urls import path
from .views import FavoriteQuoteListView, FavoriteQuoteDetailView

urlpatterns = [
    path('favorites/', FavoriteQuoteListView.as_view(), name='quote-favorites-list'),
    path('favorites/<int:pk>/', FavoriteQuoteDetailView.as_view(), name='quote-favorite-detail'),
]
