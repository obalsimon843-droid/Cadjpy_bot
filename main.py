import os
from telegram.ext import Application, CommandHandler

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update, context):
    await update.message.reply_text("Hello! Bot is LIVE on Render! 🚀")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
