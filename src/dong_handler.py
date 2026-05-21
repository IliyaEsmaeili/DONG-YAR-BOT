import message_template as mt
from src.bot_instance import bot
import stage_blue_prints as stages

def set_up_dong(call_back):
    group_name = call_back.message.chat.title
    ms = bot.send_message(call_back.from_user.id, text=mt.welcome_message_on_group_new_dong(group_name=group_name),)
    bot.register_next_step_handler(ms , stages.stage_begin , call_back.message.chat.id)