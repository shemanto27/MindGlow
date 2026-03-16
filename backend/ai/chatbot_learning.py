"""
Inner Learning Chatbot — Comprehensive educational companion.
Detailed, report-style responses for in-depth inner learning.
"""

from openai import OpenAI
from .config import get_settings, INNER_LEARNING_SYSTEM_PROMPT, CRISIS_RESOURCES, get_user_context
from .filters import detect_language, detect_crisis


class InnerLearningBot:
    """The Inner Learning chatbot - Socratic discovery companion."""
    
    def __init__(self):
        settings = get_settings()
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.conversation_history = []
        self.name = "Inner Learning"
        
    def chat(self, user_message: str, user_profile: dict = None) -> dict:
        """
        Process a user message and return a detailed educational response.
        Returns dict with: reply, language, crisis_detected, etc.
        """
        # Detect language
        language = detect_language(user_message)
        
        # Check for crisis
        crisis_indicators = detect_crisis(user_message)
        if crisis_indicators:
            return self._handle_crisis(user_message, language, crisis_indicators)
        
        # Build conversation context
        messages = [
            {"role": "system", "content": INNER_LEARNING_SYSTEM_PROMPT},
            {"role": "system", "content": get_user_context(user_profile)},
        ]
        
        if language and language != "en":
            messages.append({
                "role": "system",
                "content": f"The user is writing in '{language}'. Respond in the same language."
            })
        
        # Add conversation history
        for msg in self.conversation_history[-10:]:  # Keep last 10 exchanges
            messages.append(msg)
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        # Generate response
        reply = self._generate_response(messages)
        
        # Store in history
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": reply})
        
        return {
            "reply": reply,
            "language": language,
            "crisis_detected": False,
        }
    
    def _generate_response(self, messages):
        """Generate educational response without filtering teaching language."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=3000,  # Increased for comprehensive reports with step-by-step guidance, videos, and resources
        )
        return response.choices[0].message.content.strip()
    
    def _handle_crisis(self, user_message, language, indicators):
        """Handle crisis detection with compassionate response and redirect to appropriate resources."""
        crisis_resources = CRISIS_RESOURCES.get(language, CRISIS_RESOURCES["default"])
        
        messages = [
            {"role": "system", "content": INNER_LEARNING_SYSTEM_PROMPT},
            {"role": "system", "content": get_user_context()},
            {
                "role": "system",
                "content": " CRISIS DETECTED: Respond with deep compassion and care. Acknowledge their situation and gently redirect to crisis resources."
            },
            {"role": "user", "content": user_message}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=400,
        )
        
        compassionate_reply = response.choices[0].message.content.strip()
        
        return {
            "reply": compassionate_reply,
            "language": language,
            "crisis_detected": True,
            "crisis_resources": crisis_resources,
            "crisis_indicators": indicators,
        }
    
    def reset(self):
        """Clear conversation history."""
        self.conversation_history = []
        print(f" {self.name} conversation reset.\n")


def generate_learning_content(user_message: str, user_metadata: dict) -> dict:
    """Entry point for Django LearningView."""
    bot = InnerLearningBot()
    return bot.chat(user_message, user_profile=user_metadata)


if __name__ == "__main__":
    bot = InnerLearningBot()
    print("\nInner Learning is ready. Type your message, 'reset' to clear history, or 'quit' to exit.\n")
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() == "quit":
                print("Keep exploring.")
                break
            if user_input.lower() == "reset":
                bot.reset()
                continue
            response = bot.chat(user_input)
            print(f"\nInner Learning: {response['reply']}\n")
            if response.get("crisis_detected"):
                print(response.get("crisis_resources", ""))
        except KeyboardInterrupt:
            print("\nKeep exploring.")
            break
