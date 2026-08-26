import asyncio

import bot_instance, data, message_template as mt
import keyboards
from database.repositories import user_state_fetch, change_user_state, fetch_one, get_user_from_telegram_id, \
    execute_query
bot = bot_instance.bot


@bot.message_handler(func=lambda message : message.chat.type == "private" and message.text not in ("/start" , "/cancel" ))
async def dong_creation_router(message):
    stage = await user_state_fetch(message)
    user = await get_user_from_telegram_id(telegram_id=message.from_user.id)
    if user is None :
        raise ValueError("USER IS NONE AND TRYING TO USE THE ROUTER TO CREATE A DONG!")
    match stage :
        case "stage_begin" : await stage_begin(message , user)
        case "stage_name" : await stage_name(message, user)
        case "stage_amount" : await stage_amount(message, user)
        case "stage_participants" : await stage_participants(message, user)
        case "stage_additional_info" : await stage_additional_info(message, user)
        case "stage_confirm" : await stage_confirm(user)

async def stage_begin(message , user):
    bot_message = await bot.send_message(message.from_user.id,
                                         mt.dong_creation_main_prompt(prompt=mt.stage_name_prompt(), step=0))

    await execute_query("""UPDATE dongs
                     SET big_prompt_message = $1
                     WHERE id = $2
                  """, bot_message.id, user.dong[-1].local_dong_id)

    await change_user_state(message.from_user, "stage_name")
# @bot.callback_query_handler(lambda c : c.data == "stage_begin_start")
# async def stage_begin_start_button_handler(call_back) :
#     await change_user_state(call_back.from_user, "stage_name")
#


async def stage_name(message, user):
    user.dong[-1].name = message.text
    await execute_query("""UPDATE dongs
                     SET name = $1
                     WHERE id = $2
                  """, message.text, user.dong[-1].local_dong_id)

    bot_message_id = user.dong[-1].big_prompt_message
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=bot_message_id,
                                              text=mt.dong_creation_main_prompt(prompt=mt.stage_amount_prompt(), step=1,
                                                                                dong_name=user.dong[-1].name))
    await bot.delete_message(message_id=message.id, chat_id=message.from_user.id)
    await change_user_state(message.from_user, "stage_amount")



async def stage_amount(message, user):
    user.dong[-1].amount = message.text
    amount = None
    try :
        amount = int(message.text)
        if amount < 0 : raise ValueError
    except ValueError:
        sent_temp = await bot.send_message(chat_id=message.from_user.id , text= mt.stage_amount_validation_prompt())
        await asyncio.sleep(3)
        await bot.delete_message(chat_id=message.from_user.id , message_id=sent_temp.id)
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.id)
        return
    await execute_query("""UPDATE dongs
                     SET amount = $1
                     WHERE id = $2
                  """, amount ,  user.dong[-1].local_dong_id)
    bot_message_id = user.dong[-1].big_prompt_message
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=bot_message_id,
                                              text=mt.dong_creation_main_prompt(prompt=mt.stage_participants_prompt(),
                                                                                step=2,
                                                                                dong_name=user.dong[-1].name,
                                                                                amount=user.dong[-1].amount))
    await bot.delete_message(message_id=message.id, chat_id=message.from_user.id)
    await change_user_state(message.from_user, "stage_participants")



async def stage_participants(message, user):
    participants = message.text.split(" ")
    user.dong[-1].participants = participants
    for participant in participants :
        await execute_query("""INSERT INTO dong_participants(dong_id, user_name) VALUES ($1 , $2)
        """,user.dong[-1].local_dong_id , participant)

    bot_message_id = user.dong[-1].big_prompt_message

    await bot.edit_message_text(chat_id=message.from_user.id, message_id=bot_message_id,
                                              text=mt.dong_creation_main_prompt(
                                                  prompt=mt.stage_additional_info_prompt(), step=3,
                                                  dong_name=user.dong[-1].name,
                                                  amount=user.dong[-1].amount, participants=user.dong[-1].participants))
    await bot.delete_message(message_id=message.id, chat_id=message.from_user.id)
    await change_user_state(message.from_user, "stage_additional_info")



async def stage_additional_info(message, user):
    user.dong[-1].additional_info = message.text

    await execute_query("""UPDATE dongs
                     SET additional_info = $1
                     WHERE id = $2
                  """, message.text, user.dong[-1].local_dong_id)
    bot_message_id = user.dong[-1].big_prompt_message


    await bot.edit_message_text(chat_id=message.from_user.id, message_id=bot_message_id,
                                              text=mt.dong_creation_main_prompt(prompt=mt.stage_confirm_prompt(),
                                                                                step=4,
                                                                                dong_name=user.dong[-1].name,
                                                                                amount=user.dong[-1].amount,
                                                                                participants=user.dong[-1].participants,
                                                                                info=user.dong[-1].additional_info))
    await bot.edit_message_reply_markup(chat_id=message.from_user.id , message_id=bot_message_id , reply_markup=keyboards.stage_confirm_submit_button())
    await bot.delete_message(message_id=message.id, chat_id=message.from_user.id)
    #await change_user_state(message.from_user, "stage_confirm")



@bot.callback_query_handler(lambda call : call.data == "submit_dong")
async def dong_submit_button_handler(call_back):
    await change_user_state(telegram_id=call_back.from_user.id ,state= "stage_confirm")
    user = await get_user_from_telegram_id(telegram_id=call_back.from_user.id)
    await stage_confirm(user)

async def stage_confirm(user):
    bot_message_id = user.dong[-1].big_prompt_message
    chat_id = user.telegram_id

    await bot.edit_message_text(chat_id=chat_id, message_id=bot_message_id,
                                text=mt.dong_creation_main_prompt(prompt="فرستاده شد.", step=5,
                                                                  dong_name=user.dong[-1].name,
                                                                  amount=user.dong[-1].amount,
                                                                  participants=user.dong[-1].participants,
                                                                  info=user.dong[-1].additional_info))
    sent = await bot.send_message(chat_id=user.dong[-1].group_id, text=mt.dong_summary_main_prompt(prompt=" ", step=5,
                                                                                         dong_name=user.dong[-1].name,
                                                                                         amount=user.dong[-1].amount,
                                                                                         participants=user.dong[
                                                                                             -1].participants,
                                                                                         info=user.dong[
                                                                                             -1].additional_info , creator_name=user.full_name , creator_id=user.telegram_id) , parse_mode="HTML" )
    await execute_query("""UPDATE dongs SET last_pinned_message_id = $1 WHERE id = $2
    """ , sent.id , user.dong[-1].local_dong_id)
    await change_user_state(telegram_id= user.telegram_id, state = "stage_idle")
    try :
        await bot.pin_chat_message(chat_id=user.dong[-1].group_id , message_id=sent.id , disable_notification=False)
    except :
        await bot.send_message(chat_id=chat_id, text=mt.bot_isnt_admin_and_couldnt_pin_message())

