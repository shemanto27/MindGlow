from django.urls import path
from .views import LearningView

urlpatterns = [
    path('', LearningView.as_view(), name='learning-list-create'),
]
