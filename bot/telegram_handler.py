from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from bot.claude_handler import ask_claude, clear_history
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hola! Soy tu asistente con IA.\n"
        "Escríbeme cualquier pregunta y te responderé.\n\n"
        "📖 Comandos:\n"
        "/start - Iniciar el bot\n"
        "/help - Ver ayuda\n"
        "/clear - Borrar historial de conversación"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Comandos disponibles:\n"
        "/start - Iniciar el bot\n"
        "/help - Ver esta ayuda\n"
        "/clear - Borrar historial de conversación\n\n"
        "O simplemente escríbeme algo 💬"
    )

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    clear_history(user_id)
    await update.message.reply_text("🗑️ Historial borrado. Empezamos de cero!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_message = update.message.text
    
    await update.message.reply_text("⏳ Pensando...")
    
    # Ahora pasamos el user_id para mantener historial por usuario
    response = ask_claude(user_id, user_message)
    
    await update.message.reply_text(response)

def run_bot():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("clear", clear_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Bot iniciado con historial de conversación...")
    app.run_polling()