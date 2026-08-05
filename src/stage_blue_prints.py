import pprint

import bot_instance, data, message_template as mt
from data import Dong, User
from database.repositories import user_state_fetch, change_user_state, fetch_one, get_user_from_telegram_id, \
    execute_query

bot = bot_instance.bot  # to be more clear where bot came from


@bot.message_handler(func=lambda message: user_state_fetch(message) == "stage_begin" and message.chat.type == "private")
async def stage_begin(message):
    user = get_user_from_telegram_id(telegram_id=message.from_user.id)

    bot_message = await bot.send_message(message.from_user.id,
                                         mt.dong_creation_main_prompt(prompt=mt.stage_name_prompt(), step=0))

    execute_query("""UPDATE dongs
                     SET big_prompt_message = %s
                     WHERE id = %s
                  """, (bot_message.id, user.dong[-1].local_dong_id))

    change_user_state(message.from_user, "stage_name")


@bot.message_handler(func=lambda message: user_state_fetch(message) == "stage_name"and message.chat.type == "private")
async def stage_name(message):
    user = get_user_from_telegram_id(telegram_id=message.from_user.id)
    user.dong[-1].name = message.text
    execute_query("""UPDATE dongs
                     SET name = %s
                     WHERE id = %s
                  """, (message.text, user.dong[-1].local_dong_id))

    bot_message_id = user.dong[-1].big_prompt_message
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=bot_message_id,
                                              text=mt.dong_creation_main_prompt(prompt=mt.stage_amount_prompt(), step=1,
                                                                                dong_name=user.dong[-1].name))
    await bot.delete_message(message_id=message.id, chat_id=message.from_user.id)
    change_user_state(message.from_user, "stage_amount")


@bot.message_handler(
    func=lambda message: user_state_fetch(message) == "stage_amount" and message.chat.type == "private")
async def stage_amount(message):
    user = get_user_from_telegram_id(telegram_id=message.from_user.id)
    user.dong[-1].amount = message.text
    execute_query("""UPDATE dongs
                     SET amount = %s
                     WHERE id = %s
                  """, (message.text, user.dong[-1].local_dong_id))
    bot_message_id = user.dong[-1].big_prompt_message
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=bot_message_id,
                                              text=mt.dong_creation_main_prompt(prompt=mt.stage_participants_prompt(),
                                                                                step=2,
                                                                                dong_name=user.dong[-1].name,
                                                                                amount=user.dong[-1].amount))
    await bot.delete_message(message_id=message.id, chat_id=message.from_user.id)
    change_user_state(message.from_user, "stage_participants")


@bot.message_handler(
    func=lambda message: user_state_fetch(message) == "stage_participants" and message.chat.type == "private")
async def stage_participants(message):
    user = get_user_from_telegram_id(telegram_id=message.from_user.id)
    participants = message.text.split(" ")
    user.dong[-1].participants = participants
    for participant in participants :
        execute_query("""INSERT INTO dong_participants(dong_id, user_name) VALUES (%s , %s)
        """,(user.dong[-1].local_dong_id , participant))

    bot_message_id = user.dong[-1].big_prompt_message

    await bot.edit_message_text(chat_id=message.from_user.id, message_id=bot_message_id,
                                              text=mt.dong_creation_main_prompt(
                                                  prompt=mt.stage_additional_info_prompt(), step=3,
                                                  dong_name=user.dong[-1].name,
                                                  amount=user.dong[-1].amount, participants=user.dong[-1].participants))
    await bot.delete_message(message_id=message.id, chat_id=message.from_user.id)
    change_user_state(message.from_user, "stage_additional_info")


@bot.message_handler(
    func=lambda message: user_state_fetch(message) == "stage_additional_info" and message.chat.type == "private")
async def stage_additional_info(message):
    user = get_user_from_telegram_id(telegram_id=message.from_user.id)
    user.dong[-1].additional_info = message.text

    execute_query("""UPDATE dongs
                     SET additional_info = %s
                     WHERE id = %s
                  """, (message.text, user.dong[-1].local_dong_id))
    bot_message_id = user.dong[-1].big_prompt_message


    await bot.edit_message_text(chat_id=message.from_user.id, message_id=bot_message_id,
                                              text=mt.dong_creation_main_prompt(prompt=mt.stage_confirm_prompt(),
                                                                                step=4,
                                                                                dong_name=user.dong[-1].name,
                                                                                amount=user.dong[-1].amount,
                                                                                participants=user.dong[-1].participants,
                                                                                info=user.dong[-1].additional_info))
    await bot.delete_message(message_id=message.id, chat_id=message.from_user.id)
    change_user_state(message.from_user, "stage_confirm")


@bot.message_handler(
    func=lambda message: user_state_fetch(message) == "stage_confirm" and message.chat.type == "private")
async def stage_confirm(message):
    user = get_user_from_telegram_id(telegram_id=message.from_user.id)
    bot_message_id = user.dong[-1].big_prompt_message
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=bot_message_id,
                                text=mt.dong_creation_main_prompt(prompt="فرستاده شد.", step=5,
                                                                  dong_name=user.dong[-1].name,
                                                                  amount=user.dong[-1].amount,
                                                                  participants=user.dong[-1].participants,
                                                                  info=user.dong[-1].additional_info))
    await bot.delete_message(message_id=message.id, chat_id=message.from_user.id)
    sent = await bot.send_message(chat_id=user.dong[-1].group_id, text=mt.dong_summary_main_prompt(prompt=" ", step=5,
                                                                                         dong_name=user.dong[-1].name,
                                                                                         amount=user.dong[-1].amount,
                                                                                         participants=user.dong[
                                                                                             -1].participants,
                                                                                         info=user.dong[
                                                                                             -1].additional_info , creator_name=user.full_name , creator_id=user.telegram_id) , parse_mode="MarkdownV2")
    await bot.pin_chat_message(chat_id=user.dong[-1].group_id , message_id=sent.id , disable_notification=False)