from django.urls import path
from .views import InspirationVideoListView, PersonalizedQuoteView, FavoriteQuoteListView, FavoriteQuoteDetailView

urlpatterns = [
    path('videos/', InspirationVideoListView.as_view(), name='inspiration-videos'),
    path('quote/', PersonalizedQuoteView.as_view(), name='personalized-quote'),
    path('favorites/', FavoriteQuoteListView.as_view(), name='favorite-quotes-list'),
    path('favorites/<int:pk>/', FavoriteQuoteDetailView.as_view(), name='favorite-quote-detail'),
]
