def welcome_message_on_start():
    """

    :return:
    """

    return """سلام! ✋ به دنگ‌ یار خوش اومدی! 💸  
      
    من اینجام تا دیگه هیچ‌وقت سر حساب و کتاب دورهمی‌ها، سفرها و کافه‌ها به مشکل نخورید.  
      
    می‌تونی منو به گروهت اضافه کنی تا حواسم به دنگِ همه باشه، یا همینجا یه صورت‌حساب جدید بسازی و لینکش رو برای دوستات بفرستی.  
      
    از منوی زیر مشخص کن چیکار کنیم: 👇  
    
    """


def welcome_message_on_group_new_dong(group_name):
    return f"""
    سلام! ✋ به دنگ‌ یار خوش اومدی! 💸 
    
    من اینجام تا دیگه هیچ‌وقت سر حساب و کتاب دورهمی‌ها، سفرها و کافه‌ها به مشکل نخورید.
    
    شما در حال ساخت دنگ جدید در گروه {group_name} هستید.
    
"""


def heard_dong():
    return """شنیدم یکی گفت «دنگ»! 👀👂
    گوشام تیز شد! کسی خرجی کرده؟ اگه می‌خواید حساب و کتاب کنید و دنگ‌ها رو جمع کنید، کار رو بسپارید به من!
    کافیه مادرخرج روی دکمه زیر کلیک کنه تا پرونده این دورهمی رو باز کنیم و بیفتیم به جون بدهکارا! 💸😎
        """


def dong_creation_main_prompt(dong_name="-", amount="-", participants="-", info="-", step=0, prompt=" "):
    # Check if participants is a list, and transform it into a clean layout
    if isinstance(participants, list):
        # This joins each name with a new line and a bullet point emoji
        participants_text = "\n".join([f"  🔸 {p}" for p in participants])
    else:
        participants_text = participants

    return f"""💸 ساخت دنگ جدید

━━━━━━━━━━━━━━━━

📍 عنوان خرج
{dong_name} 

💰 مبلغ کل
{amount}

👥 افراد شریک
{participants_text}

📝 توضیحات
{info}

━━━━━━━━━━━━━━━━
{"⬜️" * (5 - step)}{"✅" * step}


{prompt}


    """


def stage_name_prompt():
    name_prompt = """بزن بریم یه دنگ جدید درست کنیم 💸
اول بگو برای چی بوده؟ اسم مکان، کافه، رستوران یا هر توضیحی که دوست داری بنویس.
مثلاً: کافه رُز، شام، سفر شمال
    """
    return name_prompt


def stage_amount_prompt():
    return """مبلغ کل این خرج چقدر بوده؟ 💰
لطفاً فقط عدد رو و به تومان وارد کن .
مثلاً: 850000
    """


def stage_participants_prompt():
    return """چه کسانی توی این دنگ شریکن؟ 👥
اسم‌ها رو بفرست یا از بین اعضا انتخاب کن.
    """


def stage_additional_info_prompt():
    return """اگر لازم می‌دونی شماره کارت، توضیح یا جزئیات بیشتر رو وارد کن 📝
مثلاً:
6037-xxxx-xxxx-xxxx
یا: سهم‌ها بعداً تسویه میشه
    """


def stage_confirm_prompt():
    return """لطفاً اطلاعات واردشده را بررسی کن.
در صورت تأیید، دنگ در گروه ارسال خواهد شد ✅
"""
