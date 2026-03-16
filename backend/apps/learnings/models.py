from django.db import models
from apps.users.models import CustomUserModel

class LearningModel(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name='learnings')
    topic = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Learning on {self.topic} for {self.user.email}"