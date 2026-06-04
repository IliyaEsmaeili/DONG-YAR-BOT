import os
from dotenv import load_dotenv
#from telebot import apihelper
import telebot

load_dotenv()
BALE_TOKEN = os.getenv("BALE_BOT_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BOT_BALE_DEEP_LINK = "https://ble.ir/dong_yar_bot?start="
BOT_TELEGRAM_DEEP_LINK = "https://t.me/dong_yaar_bot?start="
if TELEGRAM_TOKEN is None:
    raise ValueError("TELEGRAM_BOT_TOKEN is missing! Check your .env file.")

# apihelper.API_URL = "https://tapi.bale.ai/bot{0}/{1}"
bot = telebot.TeleBot(TELEGRAM_TOKEN)