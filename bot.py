import os
from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "გამარჯობა! მე შენი AI აგენტი ვარ 🤖\n\n"
        "მომწერე ნებისმიერი დავალება."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "მაგალითად:\n"
        "• მომიძებნე ბიზნეს იდეა 5000 დოლარით\n"
        "• ამიხსენი როგორ მუშაობს AI აგენტი\n"
        "• დამიწერე Python-ის კოდი"
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=user_text
        )

        answer = response.output_text

        await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text(
            "შეცდომა მოხდა. მოგვიანებით ვცადოთ."
        )
        print("ERROR:", e)


def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )

    print("AI Agent is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
