import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def ask_claude(user_message: str) -> str:
    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",  # ← modelo más barato
            max_tokens=1024,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return message.content[0].text
    
    except Exception as e:
        return f"❌ Error al contactar con Claude: {str(e)}"