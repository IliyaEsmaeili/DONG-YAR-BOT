import message_template as mt
from bot_instance import bot
import stage_blue_prints as stages

async def set_up_dong(call_back):
    group_name = call_back.message.chat.title
    ms = await bot.send_message(call_back.from_user.local_dong_id, text=mt.welcome_message_on_group_new_dong(group_name=group_name), )
    await bot.register_next_step_handler(ms, stages.stage_begin, call_back.message.chat.local_dong_id)