import os,threading
from flask import Flask
import yfinance as yf
from telegram.ext import ApplicationBuilder, CommandHandler
from datetime import datetime

TOKEN=os.environ.get("BOT_TOKEN")
flask_app=Flask(__name__)
@flask_app.route('/')
def h(): return "OK",200
@flask_app.route('/health')
def he(): return {"status":"ok"},200
def runf(): flask_app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))

def get_pred():
 df=yf.download("CADJPY=X",period="5d",interval="15m",progress=False)
 c=df['Close']; 
 last=float(c.iloc[-1])
 s20=c.rolling(20).mean().iloc[-1]
 s50=c.rolling(50).mean().iloc[-1]
 atr=(df['High']-df['Low']).rolling(14).mean().iloc[-1]
 bull=last>s20 and s20>s50
 move=float(atr*0.8)
 nxt=last+move if bull else last-move
 return last,nxt,move*100,bull

async def start(update,context):
 await update.message.reply_text("CADJPY Bot LIVE\n/signal - next 15m\n/price - now")

async def signal(update,context):
 await update.message.reply_text("Analyzing...")
 last,nxt,pips,bull=get_pred()
 dir="▲ BULLISH" if bull else "▼ BEARISH"
 msg=f"NEXT 15m: {dir}\nNow: {last:.3f}\nPred: {nxt:.3f}\nMove: {pips:.1f} pips\n{datetime.utcnow().strftime('%H:%M UTC')}"
 await update.message.reply_text(msg)

def runb():
 app=ApplicationBuilder().token(TOKEN).build()
 app.add_handler(CommandHandler("start",start))
 app.add_handler(CommandHandler("signal",signal))
 app.run_polling()

if __name__=="__main__":
 threading.Thread(target=runf,daemon=True).start()
 runb()
