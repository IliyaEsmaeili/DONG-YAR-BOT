import message_template as mt
from bot_instance import bot
from database.repositories import fetch_one
import stage_blue_prints as stages
from src.data import User



async def set_up_dong(call_back):
    group_name = call_back.message.chat.title
    await bot.send_message(call_back.from_user.id, text=mt.welcome_message_on_group_new_dong(group_name=group_name), )



