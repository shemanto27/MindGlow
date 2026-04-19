import logging
from django.apps import apps
from .config import (
    REFLECT_SYSTEM_PROMPT as STATIC_REFLECT_PROMPT,
    INNER_LEARNING_SYSTEM_PROMPT as STATIC_LEARNING_PROMPT,
)

logger = logging.getLogger(__name__)

def get_ai_prompt(prompt_name, default_text=None):
    """
    Retrieves a prompt from the database. 
    If not found, returns the default_text.
    """
    try:
        AIPrompt = apps.get_model('apps_app_settings', 'AIPrompt')
        prompt_obj = AIPrompt.objects.filter(name=prompt_name).first()
        if prompt_obj:
            return prompt_obj.prompt_text
    except Exception as e:
        logger.error(f"Error fetching prompt {prompt_name}: {e}")
    
    return default_text

def get_reflect_prompt():
    return get_ai_prompt("REFLECT_SYSTEM_PROMPT", STATIC_REFLECT_PROMPT)

def get_learning_prompt():
    return get_ai_prompt("LEARNING_SYSTEM_PROMPT", STATIC_LEARNING_PROMPT)

def get_quote_system_prompt():
    default = "You are a wisdom companion. Your task is to provide a single, deeply resonant and inspiring quote for the user."
    return get_ai_prompt("QUOTE_SYSTEM_PROMPT", default)

def get_quote_instruction_prompt():
    default = (
        "Provide a quote that matches the user's current life feeling, faith, and inspiration sources. "
        "If they mention a specific philosophy or religion, you may draw from those texts (Gita, Quran, Rumi, etc.). "
        "Return ONLY a JSON object with keys: 'quote' and 'author'."
    )
    return get_ai_prompt("QUOTE_INSTRUCTION_PROMPT", default)
