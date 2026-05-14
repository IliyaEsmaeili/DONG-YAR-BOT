import os
from dotenv import load_dotenv

import telebot
from telebot import apihelper
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()
TOKEN = os.getenv("BALE_BOT_TOKEN")
if TOKEN is None:
    raise ValueError("BALE_BOT_TOKEN is missing! Check your .env file.")
apihelper.API_URL = "https://tapi.bale.ai/bot{0}/{1}"

bot = telebot.TeleBot(TOKEN)


# ----------
# MESSAGE HANDLERS
# ----------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.type == "group":
        print("group chat /start detected")
        return
    bot.send_message(message.chat.id, """سلام! ✋ به دنگ‌ یار خوش اومدی! 💸  
  
من اینجام تا دیگه هیچ‌وقت سر حساب و کتاب دورهمی‌ها، سفرها و کافه‌ها به مشکل نخورید.  
  
می‌تونی منو به گروهت اضافه کنی تا حواسم به دنگِ همه باشه، یا همینجا یه صورت‌حساب جدید بسازی و لینکش رو برای دوستات بفرستی.  
  
از منوی زیر مشخص کن چیکار کنیم: 👇  
""", reply_markup=InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="کامند ها", callback_data="show_commands_list")
        ]
    ]))


@bot.message_handler(regexp="راهنما")
def send_bot_guid_to_gap(message):
    if message.chat.type != "group": return
    bot.reply_to(message, text="guide", reply_markup=InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="set up a dong")
        ]
    ]))


@bot.message_handler(regexp="دنگ")
def send_bot_guid_to_gap(message):
    if message.chat.type != "group": return
    bot.send_photo(message.chat.id, "./assets/heared_dong.png", """شنیدم یکی گفت «دنگ»! 👀👂
گوشام تیز شد! کسی خرجی کرده؟ اگه می‌خواید حساب و کتاب کنید و دنگ‌ها رو جمع کنید، کار رو بسپارید به من!
کافیه مادرخرج روی دکمه زیر کلیک کنه تا پرونده این دورهمی رو باز کنیم و بیفتیم به جون بدهکارا! 💸😎
    """)



# ----------
# CALL BACK HANDLERS
# ----------
@bot.callback_query_handler(func=lambda call: call.data == "show_commands_xlist")
def handle_show_commands(callback_query):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, "LIST OF COMMANDS")


bot.infinity_polling()
