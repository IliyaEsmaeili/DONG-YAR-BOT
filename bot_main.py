import telebot
import bot_instance
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import message_template as mt
import dong_handler as dong

bot = bot_instance.bot
# ----------
# MESSAGE HANDLERS
# ----------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.type == "group": return #Avoid Sending message in groups

    bot.send_message(message.chat.id, text=mt.welcome_message_on_start(), reply_markup=InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="کامند ها", callback_data="show_commands_list")
        ]
    ]))


@bot.message_handler(regexp="راهنما")
def send_bot_guid_to_gap(message):
    if message.chat.type != "group": return #Avoid Sending message in groups
    bot.reply_to(message, text="guide", reply_markup=InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="دنگ")
        ]
    ]))


@bot.message_handler(regexp="دنگ")
def send_bot_guid_to_gap(message):
    if message.chat.type != "group": return

    bot.send_photo(chat_id=message.chat.id, photo=telebot.types.InputFile("./assets/heared_dong.png", "dong_yar_bot"),
                   caption=mt.heard_dong(), reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="ایجاد دنگ جدید",

                                   callback_data="set_up_new_dong")],
             [InlineKeyboardButton(text="ربات رو استارت بزن", url="https://ble.ir/dong_yar_bot?start=")]]))


# ----------
# CALL BACK HANDLERS
# ----------
@bot.callback_query_handler(func=lambda call: call.data == "show_commands_list")
def handle_show_commands(callback_query):
    bot.answer_callback_query(callback_query.id)


@bot.callback_query_handler(func=lambda call: call.data == "set_up_new_dong")
def handle_set_up_new_dong(call_back_query):
    bot.answer_callback_query(call_back_query.id)
    dong.set_up_dong(call_back=call_back_query)


bot.infinity_polling()
