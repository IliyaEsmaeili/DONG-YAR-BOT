import pprint

import bot_instance, data, message_template as mt
from data import Dong, User

bot = bot_instance.bot  # to be more clear where bot came from
user_sessions = {}


async def stage_begin(message , group_id):
    print("begin")
    user = User(dong=Dong())
    user.telegram_id = message.from_user.local_dong_id
    user.dong.id = "dong_" + str(user.telegram_id)
    user.dong.group_id = group_id
    bot_message = await bot.send_message(message.from_user.local_dong_id,
                                         mt.dong_creation_main_prompt(prompt=mt.stage_name_prompt(), step=0))
    user.big_prompt_message = bot_message
    user_sessions[user.telegram_id] = user
    await bot.register_next_step_handler(bot_message, stage_name)


async def stage_name(message):
    user = user_sessions[message.from_user.local_dong_id]
    user.dong.name = message.text
    bot_message = user.big_prompt_message
    bot_message = await bot.edit_message_text(chat_id=message.from_user.local_dong_id, message_id=bot_message.local_dong_id,
                                              text=mt.dong_creation_main_prompt(prompt=mt.stage_amount_prompt(), step=1,
                                                            dong_name=user.dong.name))
    await bot.delete_message(message_id=message.local_dong_id, chat_id=message.from_user.local_dong_id)
    await bot.register_next_step_handler(bot_message, stage_amount)


async def stage_amount(message):
    user = user_sessions[message.from_user.local_dong_id]
    user.dong.amount = message.text
    bot_message = user.big_prompt_message
    bot_message = await bot.edit_message_text(chat_id=message.from_user.local_dong_id, message_id=bot_message.local_dong_id,
                                              text=mt.dong_creation_main_prompt(prompt=mt.stage_participants_prompt(), step=2,
                                                            dong_name=user.dong.name ,amount=user.dong.amount ))
    await bot.delete_message(message_id=message.local_dong_id, chat_id=message.from_user.local_dong_id)
    await bot.register_next_step_handler(bot_message, stage_participants)


async def stage_participants(message):
    user = user_sessions[message.from_user.local_dong_id]
    participants = message.text.split(" ")
    user.dong.participants = participants
    bot_message = user.big_prompt_message

    bot_message = await bot.edit_message_text(chat_id=message.from_user.local_dong_id, message_id=bot_message.local_dong_id,
                                              text=mt.dong_creation_main_prompt(prompt=mt.stage_additional_info_prompt(), step=3,
                                                                          dong_name=user.dong.name,
                                                                          amount=user.dong.amount , participants=user.dong.participants))
    await bot.delete_message(message_id=message.local_dong_id, chat_id=message.from_user.local_dong_id)
    await bot.register_next_step_handler(bot_message, stage_additional_info)


async def stage_additional_info(message):
    user = user_sessions[message.from_user.local_dong_id]
    user.dong.additional_info = message.text
    bot_message = user.big_prompt_message
    bot_message = await bot.edit_message_text(chat_id=message.from_user.local_dong_id, message_id=bot_message.local_dong_id,
                                              text=mt.dong_creation_main_prompt(prompt=mt.stage_confirm_prompt(), step=4,
                                                                          dong_name=user.dong.name,
                                                                          amount=user.dong.amount,
                                                                          participants=user.dong.participants , info=user.dong.additional_info))
    await bot.delete_message(message_id=message.local_dong_id, chat_id=message.from_user.local_dong_id)
    await bot.register_next_step_handler(bot_message, stage_confirm)


async def stage_confirm(message):
    user = user_sessions[message.from_user.local_dong_id]
    bot_message = user.big_prompt_message
    await bot.edit_message_text(chat_id=message.from_user.local_dong_id, message_id=bot_message.local_dong_id,
                                text=mt.dong_creation_main_prompt(prompt="فرستاده شد.", step=5,
                                                                          dong_name=user.dong.name,
                                                                          amount=user.dong.amount,
                                                                          participants=user.dong.participants,
                                                                          info=user.dong.additional_info))
    await bot.delete_message(message_id=message.local_dong_id, chat_id=message.from_user.local_dong_id)
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
    del user_sessions[message.from_user.local_dong_id]
