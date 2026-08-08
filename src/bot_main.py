import telebot
import bot_instance
import message_template as mt
import dong_handler as dong
import keyboards
from telebot.async_telebot import AsyncTeleBot
import asyncio
from data import User
from database.connection import create_pool
from database.repositories import save_user
bot = bot_instance.bot
import logging
telebot.logger.setLevel(logging.DEBUG)



# ----------
# MESSAGE HANDLERS
# ----------
@bot.message_handler(commands=['start'])
async def send_welcome(message):
    if message.chat.type in ("group" , "supergroup"): return #Avoid Sending message in groups
    print("start")
    user = User(telegram_id=message.from_user.id , full_name=message.from_user.full_name)
    print(user)
    await save_user(user)

    await bot.send_message(message.chat.id, text=mt.welcome_message_on_start(), reply_markup=keyboards.main_keyboard)
    await bot.send_message(message.chat.id, text= mt.welcome_menu_on_start(), reply_markup=keyboards.start_inline)



@bot.message_handler(regexp="دنگ")
async def send_bot_guid_to_gap(message):
    if message.chat.type not in ("group" , "supergroup") : return

    await bot.send_photo(chat_id=message.chat.id, photo=telebot.types.InputFile("../assets/heared_dong.png", "dong_yar_bot"),
                         caption=mt.heard_dong(), reply_markup=keyboards.dong_set_up)


@bot.message_handler(func=lambda message : message.text == "گیت‌هاب 💻")
async def github_info_handler(message):
    await bot.reply_to(message , mt.github_info_message())

@bot.message_handler(func=lambda message : message.text == "ربات در بله ✈️")
async def bale_bot_id_handler(message):
    await bot.reply_to(message , mt.bale_info_message())

@bot.message_handler(func=lambda message : message.text == "سازنده کیه؟ 👨‍💻")
async def developer_info_handler(message):
    await bot.reply_to(message , mt.developer_info_message())

@bot.message_handler(func=lambda message : message.text == "درباره بات 🤖")
async def bot_info_handler(message):
    await bot.reply_to(message , mt.bot_info_message())

@bot.message_handler(func=lambda message : message.text == "دونیت☕")
async def donate_info_handler(message):
    await bot.reply_to(message , mt.donate_info_message())




# ----------
# CALL BACK HANDLERS
# ----------
@bot.callback_query_handler(func=lambda call: call.data == "usage_guide")
async def handle_show_usage_guide(callback_query):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id=callback_query.from_user.id, text= mt.guide_message())

@bot.callback_query_handler(func=lambda call: call.data == "set_up_new_dong")
async def handle_set_up_new_dong(call_back_query):
    await bot.answer_callback_query(call_back_query.id)
    await dong.set_up_dong(call_back=call_back_query)

async def start_db_and_bot():
    await create_pool()
    await bot.infinity_polling()

asyncio.run(start_db_and_bot())
# bot.infinity_polling()
# asyncio.run(bot.polling())
