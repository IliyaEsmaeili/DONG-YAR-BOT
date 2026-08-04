import pprint

import bot_instance, data, message_template as mt
from data import Dong, User
from database.repositories import user_state_fetch , change_user_state , fetch_one
bot = bot_instance.bot  # to be more clear where bot came from
user_sessions = {}

@bot.message_handler(func=lambda message : user_state_fetch(message) == "stage_begin" and message.chat.type == "private")
async def stage_begin(message):
    group_id = fetch_one("""SELECT * FROM dongs WHERE creator_id = %s
    """ , (message.from_user.id, ))
    print("begin")
    user = User(dong=Dong())
    user.telegram_id = message.from_user.id
    user.dong.id = "dong_" + str(user.telegram_id)
    user.dong.group_id = group_id
    bot_message = await bot.send_message(message.from_user.id,
                                         mt.dong_creation_main_prompt(prompt=mt.stage_name_prompt(), step=0))
    user.big_prompt_message = bot_message
    user_sessions[user.telegram_id] = user
    change_user_state(message.from_user , "stage_name")


@bot.message_handler(func=lambda message : user_state_fetch(message) == "stage_name")
async def stage_name(message):
    user = user_sessions[message.from_user.id]
    user.dong.name = message.text
    bot_message = user.big_prompt_message
    bot_message = await bot.edit_message_text(chat_id=message.from_user.id, message_id=bot_message.id,
                                              text=mt.dong_creation_main_prompt(prompt=mt.stage_amount_prompt(), step=1,
                                                            dong_name=user.dong.name))
    await bot.delete_message(message_id=message.id, chat_id=message.from_user.id)
    change_user_state(message.from_user , "stage_amount")


@bot.message_handler(func=lambda message : user_state_fetch(message) == "stage_amount"and message.chat.type == "private")
async def stage_amount(message):
    user = user_sessions[message.from_user.id]
    user.dong.amount = message.text
    bot_message = user.big_prompt_message
    bot_message = await bot.edit_message_text(chat_id=message.from_user.id, message_id=bot_message.id,
                                              text=mt.dong_creation_main_prompt(prompt=mt.stage_participants_prompt(), step=2,
                                                            dong_name=user.dong.name ,amount=user.dong.amount ))
    await bot.delete_message(message_id=message.id, chat_id=message.from_user.id)
    change_user_state(message.from_user , "stage_participants")


@bot.message_handler(func=lambda message : user_state_fetch(message) == "stage_participants"and message.chat.type == "private")
async def stage_participants(message):
    user = user_sessions[message.from_user.id]
    participants = message.text.split(" ")
    user.dong.participants = participants
    bot_message = user.big_prompt_message

    bot_message = await bot.edit_message_text(chat_id=message.from_user.id, message_id=bot_message.id,
                                              text=mt.dong_creation_main_prompt(prompt=mt.stage_additional_info_prompt(), step=3,
                                                                          dong_name=user.dong.name,
                                                                          amount=user.dong.amount , participants=user.dong.participants))
    await bot.delete_message(message_id=message.id, chat_id=message.from_user.id)
    change_user_state(message.from_user , "stage_particistage_additional_infopants")


@bot.message_handler(func=lambda message : user_state_fetch(message) == "stage_additional_info"and message.chat.type == "private")
async def stage_additional_info(message):
    user = user_sessions[message.from_user.id]
    user.dong.additional_info = message.text
    bot_message = user.big_prompt_message
    bot_message = await bot.edit_message_text(chat_id=message.from_user.id, message_id=bot_message.id,
                                              text=mt.dong_creation_main_prompt(prompt=mt.stage_confirm_prompt(), step=4,
                                                                          dong_name=user.dong.name,
                                                                          amount=user.dong.amount,
                                                                          participants=user.dong.participants , info=user.dong.additional_info))
    await bot.delete_message(message_id=message.id, chat_id=message.from_user.id)
    change_user_state(message.from_user , "stage_confirm")


@bot.message_handler(func=lambda message : user_state_fetch(message) == "stage_confirm"and message.chat.type == "private")
async def stage_confirm(message):
    user = user_sessions[message.from_user.id]
    bot_message = user.big_prompt_message
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=bot_message.id,
                                text=mt.dong_creation_main_prompt(prompt="فرستاده شد.", step=5,
                                                                          dong_name=user.dong.name,
                                                                          amount=user.dong.amount,
                                                                          participants=user.dong.participants,
                                                                          info=user.dong.additional_info))
    await bot.delete_message(message_id=message.id, chat_id=message.from_user.id)
    await bot.send_message(chat_id= user.dong.group_id , text= mt.dong_creation_main_prompt(prompt=" ", step=5,
                                                                          dong_name=user.dong.name,
                                                                          amount=user.dong.amount,
                                                                          participants=user.dong.participants,
                                                                          info=user.dong.additional_info))
    data.user_list.append(user)
    # print(data.user_list)
    # pprint.pp(data.user_list.__dict__)
    for i in data.user_list:
        pprint.pp(i.__dict__)

