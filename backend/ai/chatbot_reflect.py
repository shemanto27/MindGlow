"""
Reflect Chatbot — Inner Voice for emotional exploration.
Pure non-directive questioning. No advice. Ever.
"""

from openai import OpenAI
from .config import get_settings, CRISIS_RESOURCES, get_user_context
from .prompt_loader import get_reflect_prompt
from .filters import detect_language, check_for_directives, detect_crisis


class ReflectBot:
    """The Reflect chatbot - your inner voice companion."""
    
    def __init__(self):
        settings = get_settings()
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.conversation_history = []
        self.turn_count = 0  # Track conversation turns for Clarity Moment
        self.name = "Your Inner Light"
        
    def chat(self, user_message: str, history: list = None, user_profile: dict = None) -> dict:
        """
        Process a user message and return a response.
        Returns dict with: reply, language, crisis_detected, was_filtered, etc.
        """
        # Detect language
        language = detect_language(user_message)
        
        # Check for crisis
        crisis_indicators = detect_crisis(user_message)
        if crisis_indicators:
            return self._handle_crisis(user_message, language, crisis_indicators)
        
        # Increment turn count
        self.turn_count += 1
        
        # Build conversation context
        messages = [
            {"role": "system", "content": get_reflect_prompt()},
            {"role": "system", "content": get_user_context(user_profile)},
        ]
        
        if language and language != "en":
            messages.append({
                "role": "system",
                "content": f"The user is writing in '{language}'. Respond in the same language."
            })
        
        # Inject turn-awareness so the model knows where we are in the arc
        if self.turn_count >= 7:
            messages.append({
                "role": "system",
                "content": (
                    "This is turn 7 or later. It is time for the 🌱 Clarity Moment. "
                    "Offer a gentle closing reflection with options that reference themes "
                    "from this conversation. Include a quote if it feels natural."
                )
            })
        else:
            messages.append({
                "role": "system",
                "content": f"This is turn {self.turn_count} of the exploration arc. Follow the deepening progression for this turn."
            })
        
        # Add conversation history
        session_history = history if history is not None else self.conversation_history
        for msg in session_history[-14:]:  # Keep last 14 messages (7 exchanges)
            messages.append(msg)
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        # Generate response with filtering
        reply, was_filtered, filter_reason = self._generate_with_filter(messages)
        
        # Store in history if we are using internal state
        if history is None:
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": reply})
        
        return {
            "reply": reply,
            "language": language,
            "crisis_detected": False,
            "was_filtered": was_filtered,
            "filter_reason": filter_reason,
            "turn": self.turn_count,
        }
    
    def _generate_with_filter(self, messages, max_retries=2):
        """Generate response and check for directive language."""
        was_filtered = False
        filter_reason = None
        
        for attempt in range(max_retries + 1):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=700,
            )
            reply = response.choices[0].message.content.strip()
            
            # Check for directives
            directives = check_for_directives(reply)
            if not directives:
                return reply, was_filtered, filter_reason
            
            # Directive found - retry
            if attempt < max_retries:
                messages.append({"role": "assistant", "content": reply})
                messages.append({
                    "role": "system",
                    "content": f"⚠️ VIOLATION: Your response contained directive phrases: {', '.join(directives)}. "
                            "Regenerate with ONLY open-ended questions. No advice."
                })
                was_filtered = True
                filter_reason = f"Filtered directives: {', '.join(directives)}"
            else:
                # Final attempt still has directives
                was_filtered = True
                filter_reason = f"Still contains directives after {max_retries} retries: {', '.join(directives)}"
        
        return reply, was_filtered, filter_reason
    
    def _handle_crisis(self, user_message, language, indicators):
        """Handle crisis detection with compassionate response."""
        crisis_resources = CRISIS_RESOURCES.get(language, CRISIS_RESOURCES["default"])
        
        messages = [
            {"role": "system", "content": get_reflect_prompt()},
            {"role": "system", "content": get_user_context()},
            {
                "role": "system",
                "content": "⚠️ CRISIS: Respond with deep compassion. Acknowledge their pain. NO advice. Just presence."
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
            "was_filtered": False,
        }
    
    def reset(self):
        """Clear conversation history and turn counter."""
        self.conversation_history = []
        self.turn_count = 0
        print(f" {self.name} conversation reset.\n")

    def summarize_conversation(self, history: list) -> dict:
        """Generate a title, short topic, and summary for the conversation."""
        if not history:
            return {"title": "New reflection", "topic": None, "summary": None}

        context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history[-10:]])
        
        prompt = (
            "Based on the following conversation snippets, generate:\n"
            "1. A short, poetic title (3-5 words).\n"
            "2. A single word representing the topic (e.g., 'Grief', 'Growth', 'Anxiety').\n"
            "3. A concise summary (2-3 sentences).\n\n"
            f"Conversation:\n{context}\n\n"
            "Return ONLY a JSON object with keys: title, topic, summary."
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": "You are a helpful assistant that summarizes internal reflections."},
                          {"role": "user", "content": prompt}],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            import json
            return json.loads(response.choices[0].message.content)
        except Exception:
            return {"title": history[0]['content'][:50], "topic": "Inner reflection", "summary": "A conversation about current feelings."}


def generate_ai_reply(history: list, user_message: str, user_metadata: dict) -> dict:
    """Entry point for Django ChatView."""
    bot = ReflectBot()
    # Calculate turn count from history (2 messages per turn: user + ai)
    bot.turn_count = len(history) // 2
    
    chat_response = bot.chat(user_message, history=history, user_profile=user_metadata)
    
    # Also generate metadata for the conversation
    # We update history with the new user message first to get accurate summary
    history_for_summary = history + [{"role": "user", "content": user_message}]
    metadata = bot.summarize_conversation(history_for_summary)
    chat_response.update(metadata)
    
    return chat_response


if __name__ == "__main__":
    bot = ReflectBot()
    print("\nYour Inner Light is here. Type your message, 'reset' to clear history, or 'quit' to exit.\n")
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() == "quit":
                print("Take care.")
                break
            if user_input.lower() == "reset":
                bot.reset()
                continue
            response = bot.chat(user_input)
            print(f"\nReflect: {response['reply']}\n")
            if response.get("crisis_detected"):
                print(response.get("crisis_resources", ""))
        except KeyboardInterrupt:
            print("\nTake care.")
            break
