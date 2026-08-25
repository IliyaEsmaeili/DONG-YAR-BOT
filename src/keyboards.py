from telebot.types import KeyboardButton , ReplyKeyboardMarkup , InlineKeyboardButton, InlineKeyboardMarkup
from bot_instance import BOT_TELEGRAM_DEEP_LINK
import message_template as mt
# ----------
# MAIN KEYBOARD
# ----------
_github_button = KeyboardButton(text="گیت‌هاب 💻")
_bale_button = KeyboardButton(text="ربات در بله ✈️")
_developer_button = KeyboardButton(text="سازنده کیه؟ 👨‍💻")
_about_bot_button = KeyboardButton(text="درباره بات 🤖")
_donate_button = KeyboardButton(text="دونیت☕")

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True , one_time_keyboard=False)
main_keyboard.row(_github_button, _bale_button)
main_keyboard.row(_developer_button , _about_bot_button)
main_keyboard.row(_donate_button)


# ----------
# START INLINE KEYBOARD
# ----------
start_inline = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="راهنما استفاده", callback_data="usage_guide" , style="primary")
        ]
    ])


# ----------
# HEARD DONG IN GROUP
# ----------
dong_set_up = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="ایجاد دنگ جدید",
                                   callback_data="set_up_new_dong" , style="primary")],
             [InlineKeyboardButton(text="ربات رو استارت بزن", url=BOT_TELEGRAM_DEEP_LINK , style="success")]])


# ----------
# APPROVAL MESSAGE
# ----------
def participants_to_approve(participants_list, dong_id, some_one_just_paid=None):
    # participants_as_a_2d_vertical_keyboard_button_array = [
    #     [InlineKeyboardButton(text=participant, callback_data=f"paid_(dong:{dong_id})_{participant}" , style="primary")] for participant in
    #     participants_list
    # ]
    participants_as_a_2d_vertical_keyboard_button_array = []
    if some_one_just_paid is None :
        for participant in participants_list:
            participants_as_a_2d_vertical_keyboard_button_array.append(
                [InlineKeyboardButton(text=participant, callback_data=f"paid_(dong:{dong_id})_{participant}",
                                      style="primary")])
        participants_as_a_2d_vertical_keyboard_button_array.append(
            [InlineKeyboardButton(text="تایید نمیشه", callback_data="paid_(dong:denied)", style="danger")])
    else:
        participants_as_a_2d_vertical_keyboard_button_array.append([InlineKeyboardButton(text=mt.some_one_just_payed_dong_in_reply_markup(some_one_just_paid) , style="success" , callback_data="dummy_call_back")])
        participants_as_a_2d_vertical_keyboard_button_array.append(
            [InlineKeyboardButton(text=mt.dont_press_any_reply_markup(),
                                  style="danger" , callback_data="dont_press_button")])
    # [ [] [] [] [] ]




    return participants_as_a_2d_vertical_keyboard_button_array
