from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hola! Soy tu asistente con IA.\n"
        "Escríbeme cualquier pregunta y te responderé."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Comandos disponibles:\n"
        "/start - Iniciar el bot\n"
        "/help - Ver esta ayuda\n\n"
        "O simplemente escríbeme algo 💬"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Por ahora responde con eco, luego conectaremos Claude
    user_message = update.message.text
    await update.message.reply_text(f"Recibido: {user_message}")

def run_bot():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Bot iniciado...")
    app.run_polling()