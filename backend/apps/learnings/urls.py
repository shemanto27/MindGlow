from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LearningViewSet, PastLearningListView

router = DefaultRouter()
router.register(r'', LearningViewSet, basename='learning')

urlpatterns = [
    path('past-learning/', PastLearningListView.as_view(), name='past-learning'),
    path('', include(router.urls)),
]
