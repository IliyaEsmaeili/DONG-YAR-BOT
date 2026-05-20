import os
from dotenv import load_dotenv
from telebot import apihelper
import telebot

load_dotenv()
BALE_TOKEN = os.getenv("BALE_BOT_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if BALE_TOKEN is None:
    raise ValueError("BALE_BOT_TOKEN is missing! Check your .env file.")

apihelper.API_URL = "https://tapi.bale.ai/bot{0}/{1}"
bot = telebot.TeleBot(BALE_TOKEN)