import message_template as mt
from bot_instance import bot
from database.repositories import change_user_state , save_dong
from src.data import Dong



async def set_up_dong(call_back):
    group_name = call_back.message.chat.title
    await save_dong(Dong(group_id=call_back.message.chat.id , creator_id=call_back.from_user.id))
    await change_user_state(call_back.from_user , "stage_begin")
    await bot.send_message(call_back.from_user.id, text=mt.welcome_message_on_group_new_dong(group_name=group_name), )



