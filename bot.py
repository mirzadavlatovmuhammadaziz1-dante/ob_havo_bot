import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("OPENWEATHER_API_KEY")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalom alaykum! Men ob-havo botman\n\n"
        "Shahar nomini yozing, masalan: Toshkent"
    )

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text.strip()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
    
    try:
        r = requests.get(url)
        data = r.json()
        if data["cod"] != 200:
            await update.message.reply_text("Shahar topilmadi")
            return
        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        desc = data["weather"][0]["description"].capitalize()
        await update.message.reply_text(
            f"{city.title()}\n\n"
            f"Harorat: {temp}°C (his qilish {feels}°C)\n"
            f"Holat: {desc}"
        )
    except:
        await update.message.reply_text("Xatolik yuz berdi")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, weather))
    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == '__main__':
    main()