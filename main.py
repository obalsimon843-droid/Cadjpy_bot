import os, threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot is running!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Cadjpy_bot is LIVE on FREE Render! Send /price")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("CADJPY: 110.25 (test) - FREE bot working!")

def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
