from django.db import models
from apps.users.models import CustomUserModel

class FavoriteQuoteModel(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name='favorite_quotes')
    quote = models.TextField()
    author = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quote by {self.author or 'Unknown'} saved by {self.user.email}"