from telebot.types import KeyboardButton , ReplyKeyboardMarkup , InlineKeyboardButton, InlineKeyboardMarkup

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
            InlineKeyboardButton(text="راهنما استفاده", callback_data="usage_guide")
        ]
    ])


# ----------
# HEARD DONG IN GROUP
# ----------
dong_set_up = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="ایجاد دنگ جدید",

                                   callback_data="set_up_new_dong")],
             [InlineKeyboardButton(text="ربات رو استارت بزن", url="https://ble.ir/dong_yar_bot?start=")]])