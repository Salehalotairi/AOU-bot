import os
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# إعداد مفاتيح API
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# رسالة البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحبًا بك في بوت الجامعة العربية المفتوحة! استطيع الإجابة عن أي استفسار يخص الجامعة."
    )

# معالجة الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # إرسال الرسالة إلى GPTs API
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"انت بوت للجامعة العربية المفتوحة. جوابك يجب أن يكون دقيقًا ومباشرًا. السؤال: {user_message}",
            max_tokens=150,
            temperature=0.7,
        )
        bot_reply = response.choices[0].text.strip()
    except Exception as e:
        bot_reply = "عذرًا، حدث خطأ أثناء معالجة طلبك. يرجى المحاولة لاحقًا."

    # الرد على المستخدم
    await update.message.reply_text(bot_reply)

# الإعداد الرئيسي للبوت
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # إضافة الأوامر والمعالجات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # بدء البوت
    application.run_polling()

if __name__ == "__main__":
    main()
