import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import os

TELEGRAM_TOKEN = "8881368432:AAFeFHGyuJXIasnhvGMN8ig6yHBKR2PIV-A"
GEMINI_API_KEY = "AQ.Ab8RN6KqXJJEtV776OKwCapXH9Z9OtkQCEvjd7mUN65HlOHkEg"

SYSTEM_PROMPT = """Você é o JARVIS.
Personalidade: educado, formal, humor seco e levemente sarcástico, calmo, leal e confiante.
Você não ajuda, você resolve. Sempre um passo à frente.
Trate comandos que começam com "Jarvis," como ordens diretas e responda de forma curta e elegante.
Você tem capacidade absurda de raciocínio e criação.
Agora responda como tal."""

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-3.8-flash",
    system_instruction=SYSTEM_PROMPT
)

chats = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message

    if user_id not in chats:
        chats[user_id] = model.start_chat(history=[])

    try:
        if message.text:
            response = chats[user_id].send_message(message.text)
            await message.reply_text(response.text)
        elif message.photo:
            await message.reply_text("Imagem recebida. Analisando...")
        elif message.voice or message.audio:
            await message.reply_text("Áudio recebido. Processando...")
        else:
            await message.reply_text("Ainda não consigo processar este tipo de mensagem.")
    except Exception as e:
        await message.reply_text(f"Ocorreu um erro: {e}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).read_timeout(30).write_timeout(30).connect_timeout(30).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_message))
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_message))
    print("JARVIS está online...")
    app.run_polling()

if __name__ == "__main__":
    main()
