import os
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحبًا بك في بوت الجامعة العربية المفتوحة! استطيع الإجابة عن أي استفسار يخص الجامعة."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"انت بوت للجامعة العربية المفتوحة. جوابك يجب أن يكون دقيقًا ومباشرًا. السؤال: {user_message}",
            max_tokens=150,
            temperature=0.7,
        )
        bot_reply = response.choices[0].text.strip()
    except Exception:
        bot_reply = "عذرًا، حدث خطأ أثناء معالجة طلبك. يرجى المحاولة لاحقًا."
    await update.message.reply_text(bot_reply)

@app.route(f'/{TELEGRAM_BOT_TOKEN}', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), app.bot)
    await app.process_update(update)
    return "ok"

@app.route('/setwebhook', methods=['GET'])
async def set_webhook():
    webhook_url = f"{WEBHOOK_URL}/{TELEGRAM_BOT_TOKEN}"
    await app.bot.set_webhook(webhook_url)
    return f"Webhook set to {webhook_url}", 200

def main():
    global app
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run(port=5000)

if __name__ == "__main__":
    main()
