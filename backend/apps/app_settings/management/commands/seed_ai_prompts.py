from django.core.management.base import BaseCommand
from apps.app_settings.models import AIPrompt
from ai.config import REFLECT_SYSTEM_PROMPT, INNER_LEARNING_SYSTEM_PROMPT

class Command(BaseCommand):
    help = 'Seed the database with initial AI prompts'

    def handle(self, *args, **options):
        prompts = [
            {
                "name": "REFLECT_SYSTEM_PROMPT",
                "prompt_text": REFLECT_SYSTEM_PROMPT,
                "description": "System prompt for the Reflect (Inner Voice) chatbot."
            },
            {
                "name": "LEARNING_SYSTEM_PROMPT",
                "prompt_text": INNER_LEARNING_SYSTEM_PROMPT,
                "description": "System prompt for the Inner Learning educational chatbot."
            },
            {
                "name": "QUOTE_SYSTEM_PROMPT",
                "prompt_text": "You are a wisdom companion. Your task is to provide a single, deeply resonant and inspiring quote for the user.",
                "description": "System prompt for the personalized quote generator."
            },
            {
                "name": "QUOTE_INSTRUCTION_PROMPT",
                "prompt_text": "Provide a quote that matches the user's current life feeling, faith, and inspiration sources. If they mention a specific philosophy or religion, you may draw from those texts (Gita, Quran, Rumi, etc.). Return ONLY a JSON object with keys: 'quote' and 'author'.",
                "description": "Specific JSON instructions for the quote generator."
            }
        ]

        for p in prompts:
            obj, created = AIPrompt.objects.update_or_create(
                name=p["name"],
                defaults={
                    "prompt_text": p["prompt_text"],
                    "description": p["description"]
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created prompt: {p["name"]}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Successfully updated prompt: {p["name"]}'))
