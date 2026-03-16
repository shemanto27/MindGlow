from django.db import models

class FAQModel(models.Model):
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"FAQ (Updated: {self.updated_at.date()})"

class PrivacyPolicyModel(models.Model):
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Privacy Policy (Updated: {self.updated_at.date()})"

class TermsAndConditionsModel(models.Model):
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Terms and Conditions (Updated: {self.updated_at.date()})"

class SupportMessageModel(models.Model):
    subject = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Support: {self.subject} from {self.email}"