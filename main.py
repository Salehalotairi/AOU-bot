import os
import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# إعداد مفاتيح API
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# إعداد OpenAI API
openai.api_key = OPENAI_API_KEY

# رسالة البداية
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "مرحبًا بك في بوت الجامعة العربية المفتوحة! استطيع الإجابة عن أي استفسار يخص الجامعة."
    )

# معالجة الرسائل
def handle_message(update: Update, context: CallbackContext):
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
    update.message.reply_text(bot_reply)

# الإعداد الرئيسي للبوت
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher

    # إضافة الأوامر والمعالجات
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
