from django.db import models

class AIPrompt(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Unique name for the prompt")
    prompt_text = models.TextField(help_text="The actual system prompt content")
    description = models.TextField(blank=True, null=True, help_text="Description of where this prompt is used")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "AI Prompt"
        verbose_name_plural = "AI Prompts"
        db_table = 'ai_prompts'