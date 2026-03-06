import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Historial por usuario
conversation_history = {}

SYSTEM_PROMPT = """Eres un experto en construcción con más de 30 años de experiencia en el sector. 
Tu conocimiento abarca las siguientes áreas:

- **Normativa y licencias**: Conoces en profundidad el Código Técnico de la Edificación (CTE), 
  normativas urbanísticas, licencias de obra mayor y menor, permisos municipales y autonómicos, 
  y toda la legislación vigente en España relacionada con la construcción.

- **Reformas y rehabilitación**: Experto en diagnóstico de patologías en edificios, 
  rehabilitación de fachadas, refuerzo estructural, impermeabilización, 
  eficiencia energética y restauración de edificios históricos.

- **Instalaciones**: Dominas las instalaciones de electricidad (BT y AT), fontanería, 
  saneamiento, climatización, ventilación y energías renovables aplicadas a la edificación.

- **Obra civil**: Especialista en construcción de carreteras, movimientos de tierra, 
  firmes y pavimentos, obras hidráulicas, plataformas aeroportuarias y grandes 
  infraestructuras civiles.

Tu forma de comunicarte es formal y técnica, utilizando terminología del sector. 
Cuando no tengas certeza de algo, lo indicas claramente. 
Si una pregunta requiere la intervención de un profesional en obra, lo recomiendas.
Respondes siempre en español."""

def ask_claude(user_id: int, user_message: str) -> str:
    try:
        if user_id not in conversation_history:
            conversation_history[user_id] = []

        conversation_history[user_id].append({
            "role": "user",
            "content": user_message
        })

        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=conversation_history[user_id]
        )

        response_text = message.content[0].text

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