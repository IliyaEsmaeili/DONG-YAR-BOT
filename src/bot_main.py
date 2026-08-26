import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import bot_instance
import message_template as mt
import dong_handler as dong
import keyboards
import asyncio
from data import User
from database.connection import create_pool
from database.repositories import save_user, fetch_one, fetch_all, execute_query

bot = bot_instance.bot

import logging
telebot.logger.setLevel(logging.DEBUG)

# ----------
# SMALL STORAGE TO KEEP SOME FILE IDS
# ----------
asset_file_ids_cache = {
}
asset_file_ids_cache_lock = asyncio.Lock()
bot_info = None


# ----------
# MESSAGE HANDLERS
# ----------
@bot.message_handler(commands=['start'])
async def send_welcome(message):
    if message.chat.type in ("group", "supergroup"): return  # Avoid Sending message in groups
    user = User(telegram_id=message.from_user.id, full_name=message.from_user.full_name)
    await save_user(user)

    await bot.send_message(message.chat.id, text=mt.welcome_message_on_start(), reply_markup=keyboards.main_keyboard)
    await bot.send_message(message.chat.id, text=mt.welcome_menu_on_start(), reply_markup=keyboards.start_inline)


@bot.message_handler(regexp=r"^دنگ$")
async def send_bot_guid_to_gap(message):
    if message.chat.type not in ("group", "supergroup"): return

    if "heard_dong_asset" not in asset_file_ids_cache:
        sent_message = await  bot.send_photo(chat_id=message.chat.id,
                                             photo=telebot.types.InputFile("../assets/heared_dong.png", "dong_yar_bot"),
                                             caption=mt.heard_dong(), reply_markup=keyboards.dong_set_up)
        async with asset_file_ids_cache_lock:
            asset_file_ids_cache["heard_dong_asset"] = sent_message.photo[-1].file_id
    else:
        await bot.send_photo(chat_id=message.chat.id,
                             photo=asset_file_ids_cache["heard_dong_asset"],
                             caption=mt.heard_dong(), reply_markup=keyboards.dong_set_up)


# ----------
# receipt check
# ----------
import pprint


@bot.message_handler(func=lambda
        message: message.reply_to_message is not None and message.reply_to_message.from_user.id == bot_info.id and any(
    word in message.text for word in ["پرداخت دنگ"]))
@bot.message_handler(content_types=['photo', 'document'], func=lambda
        message: message.reply_to_message is not None and message.reply_to_message.from_user.id == bot_info.id)
async def reply_to_send_receipt_handler(message):
    fetch_dong_and_creator = await fetch_one(
        """SELECT d.id, d.name, d.amount, d.creator_id, u.full_name, d.group_id, d.group_name
           FROM dongs d
                    JOIN users u ON u.telegram_id = d.creator_id
           WHERE group_id = $1
             AND last_pinned_message_id = $2
        """, message.chat.id, message.reply_to_message.message_id)
    fetch_dongs_participants = await fetch_all("""SELECT *
                                                  FROM dong_participants
                                                  WHERE dong_id = $1
                                               """, fetch_dong_and_creator['id'])

    participants_list = [participants['user_name'] for participants in fetch_dongs_participants]
    not_paid_participants_list = [participants['user_name'] for participants in fetch_dongs_participants if
                                  participants["has_paid"] == False]

    if fetch_dong_and_creator is not None:
        await bot.forward_message(from_chat_id=fetch_dong_and_creator['group_id'],
                                  chat_id=fetch_dong_and_creator['creator_id'], message_id=message.message_id)
        await bot.send_message(chat_id=fetch_dong_and_creator['creator_id'],
                               text=mt.dong_receipt_approval_message(dong_name=fetch_dong_and_creator['name'],
                                                                     amount_per_person=fetch_dong_and_creator[
                                                                                           'amount'] / len(
                                                                         participants_list),

                                                                     reciept_sender_info=mt.receipt_sender_info(
                                                                         receipt_sender_full_name=message.from_user.full_name,
                                                                         receipt_sender_id=message.from_user.id,
                                                                         receipt_sender_user_name=message.from_user.username),
                                                                     participants_list=participants_list,
                                                                     group_name=fetch_dong_and_creator['group_name'],

                                                                     unpaid_list=not_paid_participants_list),
                               reply_markup=InlineKeyboardMarkup(
                                   keyboards.participants_to_approve(not_paid_participants_list,
                                                                     fetch_dong_and_creator['id'])))


# ----------
# KEYBOARD BUTTONS
# ----------
@bot.message_handler(func=lambda message: message.text == "گیت‌هاب 💻")
async def github_info_handler(message):
    await bot.reply_to(message, mt.github_info_message())


@bot.message_handler(func=lambda message: message.text == "ربات در بله ✈️")
async def bale_bot_id_handler(message):
    await bot.reply_to(message, mt.bale_info_message())


@bot.message_handler(func=lambda message: message.text == "سازنده کیه؟ 👨‍💻")
async def developer_info_handler(message):
    await bot.reply_to(message, mt.developer_info_message())


@bot.message_handler(func=lambda message: message.text == "درباره بات 🤖")
async def bot_info_handler(message):
    await bot.reply_to(message, mt.bot_info_message())


@bot.message_handler(func=lambda message: message.text == "دونیت☕")
async def donate_info_handler(message):
    await bot.reply_to(message, mt.donate_info_message())


# ----------
# CALL BACK HANDLERS
# ----------
@bot.callback_query_handler(func=lambda call: call.data == "usage_guide")
async def handle_show_usage_guide(callback_query):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id=callback_query.from_user.id, text=mt.guide_message())


@bot.callback_query_handler(func=lambda call: call.data == "set_up_new_dong")
async def handle_set_up_new_dong(call_back_query):
    await bot.answer_callback_query(call_back_query.id)
    await dong.set_up_dong(call_back=call_back_query)


@bot.callback_query_handler(func=lambda call: call.data.startswith("paid_(dong:"))
async def handle_receipt_approval(call_back_query):
    rest = call_back_query.data.removeprefix("paid_(dong:")
    dong_id_str, payer_name = rest.split(")_", 1)
    dong_id = int(dong_id_str)
    await execute_query("""UPDATE dong_participants
                           SET has_paid = TRUE
                           WHERE dong_id = $1
                             AND user_name = $2
                        """, dong_id, payer_name)

    dong_info = await fetch_one("""SELECT d.*, u.full_name, u.telegram_id
                                   FROM dongs d
                                            JOIN users u ON d.creator_id = u.telegram_id
                                   WHERE d.id = $1
                                """, dong_id)
    participants_info = await fetch_all("""SELECT *
                                           FROM dong_participants
                                           WHERE dong_id = $1
                                        """, dong_id)
    participants_list = [participants['user_name'] for participants in participants_info]
    not_paid_participants_list = [participants['user_name'] for participants in participants_info if
                                  participants["has_paid"] == False]
    if payer_name in not_paid_participants_list:
        not_paid_participants_list.remove(payer_name)

    try:
        await bot.edit_message_text(chat_id=dong_info['group_id'], message_id=dong_info['last_pinned_message_id'],
                                    text=mt.dong_summary_main_prompt(dong_name=dong_info['name'], amount=dong_info[
                                        'amount'], participants=participants_list, info=dong_info['additional_info'],
                                                                     creator_name=dong_info['full_name'],
                                                                     creator_id=dong_info['telegram_id'],
                                                                     unpaid_list=not_paid_participants_list),
                                    parse_mode="HTML")
        await bot.send_message(chat_id=dong_info['group_id'], reply_to_message_id=dong_info['last_pinned_message_id'],
                               text=mt.thanks_for_paying_and_unpaid_list(payer_name, not_paid_participants_list))
        await bot.send_message(chat_id=call_back_query.from_user.id,
                               text=mt.the_new_payment_was_successfully_notified_in_group(True))


    except Exception as e:
        print(e)
        new_message = await bot.send_message(chat_id=dong_info['group_id'],
                                             text=mt.dong_summary_main_prompt(dong_name=dong_info['name'],
                                                                              amount=dong_info[
                                                                                  'amount'],
                                                                              participants=participants_list,
                                                                              info=dong_info['additional_info'],
                                                                              creator_name=dong_info['full_name'],
                                                                              creator_id=dong_info['telegram_id'],
                                                                              unpaid_list=not_paid_participants_list),
                                             parse_mode="HTML")

        await bot.send_message(chat_id=dong_info['group_id'],
                               text=mt.thanks_for_paying_and_unpaid_list(payer_name, not_paid_participants_list),
                               reply_to_message_id=new_message.id)
        last_pinned_message_before_change = dong_info['last_pinned_message_id']
        await execute_query("""UPDATE dongs
                               SET last_pinned_message_id = $1
                               WHERE id = $2
                            """, new_message.id, dong_id)
        await bot.send_message(chat_id=call_back_query.from_user.id,
                               text=mt.the_new_payment_was_successfully_notified_in_group(False))
        try:
            try:
                await bot.unpin_chat_message(chat_id=dong_info['group_id'],
                                             message_id=last_pinned_message_before_change)
            except Exception as e:
                await bot.send_message(chat_id=dong_info['creator_id'], text=mt.couldnt_unpin_last_pinned_message())
            await bot.pin_chat_message(chat_id=dong_info['group_id'], message_id=new_message.id,
                                       disable_notification=False)

        except:
            await bot.send_message(chat_id=dong_info['creator_id'], text=mt.bot_isnt_admin_and_couldnt_pin_message())
    await bot.edit_message_text(chat_id=dong_info['creator_id'], message_id=call_back_query.message.id,
                                text=mt.dong_receipt_approval_message(dong_name=dong_info['name'],
                                                                      amount_per_person=dong_info['amount'] / len(
                                                                          participants_list),
                                                                      reciept_sender_info=mt.reciept_senders_recipet_was_approved(
                                                                          payer_name),
                                                                      group_name=dong_info['group_name'],
                                                                      unpaid_list=not_paid_participants_list,
                                                                      prompt=mt.you_approved_this_dong_before(),
                                                                      participants_list=participants_list))
    await bot.edit_message_reply_markup(chat_id=dong_info['creator_id'], message_id=call_back_query.message.id,
                                        reply_markup=InlineKeyboardMarkup(
                                            keyboards.participants_to_approve(participants_list, dong_id,
                                                                              some_one_just_paid=payer_name)))


async def start_db_and_bot():
    await create_pool()
    global bot_info
    bot_info = await bot_instance.get_bot_info()  # fill bot info
    await bot.infinity_polling()


# ----------
# STAGES
# ----------
import stage_blue_prints

asyncio.run(start_db_and_bot())
