import os, threading, datetime
import yfinance as yf
import pandas as pd
import numpy as np
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "CADJPY Bot LIVE!"

def get_signal():
    try:
        df = yf.Ticker("CADJPY=X").history(period="2d", interval="15m")
        if len(df) < 30:
            return "Not enough data"

        close = df['Close']
        high = df['High']
        low = df['Low']

        # EMA 9/21
        ema9 = close.ewm(span=9).mean().iloc[-1]
        ema21 = close.ewm(span=21).mean().iloc[-1]

        # RSI 14
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        rsi_val = rsi.iloc[-1]

        # ATR 14
        tr = pd.concat([high-low, (high-close.shift()).abs(), (low-close.shift()).abs()], axis=1).max(axis=1)
        atr = tr.rolling(14).mean().iloc[-1]

        price = close.iloc[-1]
        now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

        # Logic
        if ema9 < ema21 and rsi_val < 45:
            signal = "▼ SELL · SHORT"
            confidence = 80 if rsi_val < 40 else 65
            sl = price + atr*1.2
            tp = price - atr*2
        elif ema9 > ema21 and rsi_val > 55:
            signal = "▲ BUY · LONG"
            confidence = 80 if rsi_val > 60 else 65
            sl = price - atr*1.2
            tp = price + atr*2
        else:
            signal = "■ NEUTRAL · WAIT"
            confidence = 50
            sl = price + atr*1.2
            tp = price - atr*1.2

        text = f"""CADJPY signal
{signal}

Price: {price:.3f}
Confidence: {confidence}%
RSI (14): {rsi_val:.1f}
EMA (9/21): {ema9:.3f} / {ema21:.3f}
ATR (14): {atr:.3f}

Stop loss: {sl:.3f}
Take profit: {tp:.3f}

15-minute candles · generated
{now}

Educational market analysis only. Not financial advice."""
        return text
    except Exception as e:
        return f"Error getting data: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ CADJPY Bot Online!\nUse /signal to get live signal\n/price for quick price")

async def signal_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Analyzing 15m chart...")
    msg = get_signal()
    await update.message.reply_text(msg)

async def price_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = get_signal()
    # just send first 3 lines for quick
    await update.message.reply_text(msg.split('\n\n')[0] + "\n" + msg.split('\n')[2])

def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal_cmd))
    app.add_handler(CommandHandler("price", price_cmd))
    app.add_handler(CommandHandler("analysis", signal_cmd))
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
