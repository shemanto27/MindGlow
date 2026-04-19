"""
MindGlow Quote Generator — Personalized wisdom and inspiration.
"""

from openai import OpenAI
from .config import get_settings, get_user_context
from .prompt_loader import get_quote_system_prompt, get_quote_instruction_prompt

class QuoteGenerator:
    """Generates personalized inspiring quotes based on user profile."""
    
    def __init__(self):
        settings = get_settings()
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        
    def generate_quote(self, user_profile: dict = None) -> dict:
        """
        Generate a personalized quote.
        Returns dict with: quote, author.
        """
        messages = [
            {"role": "system", "content": get_quote_system_prompt()},
            {"role": "system", "content": get_user_context(user_profile)},
            {
                "role": "system",
                "content": get_quote_instruction_prompt()
            },
            {"role": "user", "content": "Give me a quote that speaks to my heart today."}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.8,
                response_format={"type": "json_object"}
            )
            import json
            return json.loads(response.choices[0].message.content)
        except Exception:
            # Fallback quote
            return {
                "quote": "The wound is the place where the Light enters you.",
                "author": "Rumi"
            }

def generate_personalized_quote(user_metadata: dict) -> dict:
    """Entry point for Django Inspiration API."""
    generator = QuoteGenerator()
    return generator.generate_quote(user_profile=user_metadata)
