import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Diccionario para guardar el historial por usuario
conversation_history = {}

def ask_claude(user_id: int, user_message: str) -> str:
    try:
        # Inicializar historial si es la primera vez
        if user_id not in conversation_history:
            conversation_history[user_id] = []
        
        # Añadir mensaje del usuario al historial
        conversation_history[user_id].append({
            "role": "user",
            "content": user_message
        })
        
        # Llamada a Claude con todo el historial
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=conversation_history[user_id]
        )
        
        response_text = message.content[0].text
        
        # Guardar respuesta de Claude en el historial
        conversation_history[user_id].append({
            "role": "assistant",
            "content": response_text
        })
        
        return response_text
    
    except Exception as e:
        return f"❌ Error al contactar con Claude: {str(e)}"

def clear_history(user_id: int):
    """Borra el historial de un usuario"""
    if user_id in conversation_history:
        del conversation_history[user_id]