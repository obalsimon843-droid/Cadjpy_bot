import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Cadjpy_bot is LIVE! Send /price for CADJPY")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("CADJPY: 110.25 (test) - Bot working!")

def main():
    if not TOKEN:
        print("ERROR: BOT_TOKEN missing!")
        return
    print("Bot starting...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    app.run_polling()

if __name__ == "__main__":
    main()
