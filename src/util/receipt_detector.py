#iliya : this module is ChatGPT generated :_)

import re

RECEIPT_KEYWORDS = {

    "کارت به کارت": 3,
    "انتقال وجه": 3,
    "واریز": 2,
    "برداشت": 2,
    "پرداخت": 2,
    "تراکنش": 2,


    "مبلغ": 3,
    "ریال": 2,
    "تومان": 2,


    "شماره پیگیری": 4,
    "کد پیگیری": 4,
    "شماره مرجع": 4,
    "شماره ارجاع": 4,
    "شماره سند": 4,
    "کد رهگیری": 4,
    "شناسه پرداخت": 4,


    "سپرده": 2,
    "کارت": 1,
    "حساب": 1,
    "شبا": 2,


    "به نام": 2,
    "گیرنده": 2,
    "صاحب حساب": 2,

    "موفق": 2,
    "موفقیت آمیز": 2,
    "انجام شد": 2,
    "تایید شد": 2,
}

BANK_NAMES = [
    "ملی", "ملت", "تجارت", "صادرات", "سپه",
    "پاسارگاد", "آینده", "سامان", "پارسیان",
    "اقتصاد نوین", "شهر", "سینا", "دی",
    "رفاه", "کشاورزی", "مسکن", "گردشگری",
    "بلو", "بلوبانک", "مهر ایران", "رسالت",
    "کارافرین" ,
]

def is_bank_receipt(text: str) -> bool:
    if not text:
        return False

    score = 0

    text = text.replace("ي", "ی").replace("ك", "ک")

    for keyword, weight in RECEIPT_KEYWORDS.items():
        if keyword in text:
            score += weight

    # Bank names
    for bank in BANK_NAMES:
        if bank in text:
            score += 2

    # Card number pattern
    if re.search(r"\d{4}[-\s*]?\d{4}[-\s*]?\d{4}[-\s*]?\d{4}", text):
        score += 3

    # Large monetary amount
    if re.search(r"\d[\d,]{4,}", text):
        score += 2

    # Date
    if re.search(r"\d{4}/\d{1,2}/\d{1,2}", text):
        score += 2

    # Time
    if re.search(r"\d{1,2}:\d{2}", text):
        score += 1

    return score >= 8