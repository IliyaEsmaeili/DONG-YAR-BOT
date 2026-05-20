import bot_instance
import data

bot = bot_instance.bot #to be more clear where bot came from
import message_template as mt
from data import Dong, User

user_sessions = {}




def stage_begin(message):
    user = User(dong=Dong())
    user.messanger_id = message.from_user.id
    user.dong.id =   "dong_" + str(user.messanger_id)
    user_sessions[user.messanger_id] = user
    ms = bot.send_message(message.from_user.id, mt.stage_name_prompt())
    bot.register_next_step_handler(ms , stage_name)

def stage_name(message):
    user = user_sessions.get(message.from_user.id)
    user.dong.name = message.text
    ms = bot.send_message(message.from_user.id, mt.stage_amount_prompt())
    bot.register_next_step_handler(ms , stage_amount)

def stage_amount(message):
    user = user_sessions.get(message.from_user.id)
    user.dong.amount = message.text
    ms = bot.send_message(message.from_user.id, mt.stage_participants_prompt())
    bot.register_next_step_handler(ms, stage_participants)

def stage_participants(message):
    user = user_sessions.get(message.from_user.id)
    participants = message.text.split(" ")
    user.dong.participants = participants
    ms = bot.send_message(message.from_user.id, mt.stage_additional_info_prompt())
    bot.register_next_step_handler(ms, stage_additional_info)


def stage_additional_info(message):
    user = user_sessions.get(message.from_user.id)
    user.dong.additional_info = message.text
    ms = bot.send_message(message.from_user.id , mt.stage_confirm_prompt())
    bot.register_next_step_handler(ms,  stage_confirm)

def stage_confirm(message):
    user = user_sessions.get(message.from_user.id)
    data.user_list.append(user)
    print(data.user_list)
    del user_sessions[message.from_user.id]