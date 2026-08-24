

def welcome_message_on_start():
    return """سلام! ✋ به دنگ‌ یار خوش اومدی! 💸  
      
من اینجام تا دیگه سر حساب و کتاب دورهمی‌ها، سفرها و کافه‌ها به مشکل نخورید. 
      
می‌تونی منو به گروهت اضافه کنی تا حواسم به دنگِ همه باشه، یا همینجا یه صورت‌حساب جدید بسازی و لینکش رو برای دوستات بفرستی."""
# " " taghir space

def welcome_menu_on_start():
    return "از منوی زیر مشخص کن چیکار کنیم: 👇"

def welcome_message_on_group_new_dong(group_name):
    return f"""
    سلام! ✋ به دنگ‌ یار خوش اومدی! 💸 
    
    من اینجام تا دیگه سر حساب و کتاب دورهمی‌ها، سفرها و کافه‌ها به مشکل نخورید.
    
    شما در حال ساخت دنگ جدید در گروه {group_name} هستید.
    
    در صورت تایید کلمه شروع را ارسال کنید:
"""


def heard_dong():
    return """شنیدم یکی گفت «دنگ»! 👀👂
    اگه می‌خواید حساب و کتاب کنید و دنگ‌ها رو جمع کنید، کار رو بسپارید به من!
    کافیه مادرخرج روی دکمه زیر کلیک کنه تا دنگ هر شخص رو حساب کنیم و بیفتیم به جون بدهکارا! 💸😎
        """


def dong_creation_main_prompt(dong_name="-", amount="-", participants="-", info="-", step=0, prompt=" " , stage = None):
    if stage is not None :
        match stage :
            case "stage_begin" :
                step = 0
            case "stage_name":
                step = 1
            case "stage_amount":
                step = 2
            case "stage_participants":
                step = 3
            case "stage_additional_info":
                step = 4
            case "stage_confirm":
                step = 5

    if isinstance(participants, list):
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
def dong_summary_main_prompt(dong_name="-", amount= None, participants="-", info="-", step=0, prompt=" " , stage = None , creator_name = None , creator_id = None ) :
    if stage is not None :
        match stage :
            case "stage_begin" :
                step = 0
            case "stage_name":
                step = 1
            case "stage_amount":
                step = 2
            case "stage_participants":
                step = 3
            case "stage_additional_info":
                step = 4
            case "stage_confirm":
                step = 5

    # Check if participants is a list, and transform it into a clean layout
    if isinstance(participants, list):
        # This joins each name with a new line and a bullet point emoji
        participants_text = "\n".join([f"  🔸 {p}" for p in participants])
    else:
        participants_text = participants

    return f"""💸دنگ جدید از راه رسید

━━━━━━━━━━━━━━━━
💳مادر خرج
<a href="tg://user?id={creator_id}">{creator_name}</a>
📍 عنوان خرج
{dong_name} 

💰 مبلغ کل
{amount}

👥 افراد شریک
{participants_text}

💰 بدهی هر نفر
{int(amount / len(participants)) if participants else "err"}
📝 توضیحات
{info}

━━━━━━━━━━━━━━━━



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
لطفاً فقط عدد رو و به هزار تومان وارد کن(به لاتین) .
مثلاً: 850000
    """

def stage_amount_validation_prompt():
    return "لطفا عدد رو به صورت انگلیسی و 'هزار تومان' وارد کنید."

def stage_participants_prompt():
    return """چه کسانی توی این دنگ شریکن؟ 👥
اسم‌ها رو بفرست یا از بین اعضا انتخاب کن.
لطفا اسم هر شخص بدون فاصله بنویس
برای مثال: محمدرضا یا محمد-رضا-احمدی درست و محمد رضا اشتباهه

پس جمعا مثلا ۲ نفر اینجوری میشه 
محمد-رضا-قربانی سارا-محمدی
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

در صورت تایید، کلمه 'تایید' را ارسال کنید:
"""



def guide_message():
    return """اینجا بهت یاد میدم چطوری حساب‌کتاب‌های گروه رو مثل آب خوردن مدیریت کنی:
قدم اول: منو ببر تو گروهت! 🚀
کافیه بری تو پروفایل من (همین ربات)، دکمه “Add to Group” یا “افزودن به گروه” رو بزنی و گروه مورد نظرت رو انتخاب کنی.
(اگر نبود برو توی گروهتون و اونجا من رو اضافه کن(یادت نره start من رو زده باشی))


قدم دوم: چرا بهتره ادمین باشم؟💻 
برای اینکه وقتی کسی گفت «دنگ» سریع پیدام بشه و یا لیست بدهکارها رو پیام‌سنجاق (Pin) کنم، حتماً منو تو گروهت ادمین کن. (نگران نباش، دست به چیزی نمیزنم، من فقط دنبال پولم! 🥸)

قدم سوم: کلمه جادوییِ «دنگ» 🪄
هر وقت جایی خرجی کردید، کافیه یک نفر تو چت بنویسه: دنگ
من همون لحظه ظاهر میشم!

قدم چهارم: مادرخرج وارد می‌شود! 😎
وقتی من پیدام شد، کسی که پول رو حساب کرده روی دکمه‌ی پیام من کلیک می‌کنهو من اونجا اطلاعات مورد نیازو ازش می‌پرسم:
شماره کارتت چیه؟ 💳
چند نفر باید پول بدن؟ 👥 و ….

قدم پنجم: تسویه حساب و فیش واریزی 🧾
حالا لیست آماده‌ست! هرکسی که سهمش رو کارت‌به‌کارت کرد، کافیه عکس فیش واریزی رو تو گروه روی لیست من ریپلای کنه . هروقت فیش تایید شد، اسمش رو از لیست بدهکارا خط می‌زنم و می‌گم چقدر از پول جمع شده و کیا هنوز پیچوندن!

💡 نکته مهم: مادرخرج می‌تونه هر زمان که خواست با زدن یک دکمه، به بدهکارا پیام هشدار بفرسته تا زودتر پول رو بزنن!
بزن بریم که هیچ پولی نباید رو زمین بمونه! 💸💪
    """




def github_info_message() :
    return """این پروژه کاملا Open Source منتشر شده.💻

شما میتونید کدها رو ببینید، فورک کنید، تغییر بدید و واسه خودتون شخصی‌سازی کنید.

اگه باگی دیدید، پیشنهادی داشتید یا خواستید فیچر جدیدی اضافه کنید، حتما تو گیت‌هاب Issue بزنید یا PR (Pull Request) بدید تا با هم بررسیش کنیم. 

🔗 لینک ریپازیتوری گیت هاب بات:
https://github.com/IliyaEsmaeili/DONG-YAR-BOT

⭐️ اگه با بات حال کردید یا کدها به دردتون خورد، با یه Star دادن به ریپو خستگی یه نرد رو در میکنید! 🤓"""


def telegram_info_message():
    return """این ربات همزمان توی تلگرام هم با قدرت فعال و در دسترسه! 🚀

اگه اونجا راحت‌تری، میتونی از طریق آیدی زیر پیداش کنی و دنگ‌هات رو اونجا مدیریت کنی:

🆔 @dong_yaar_bot"""
def bale_info_message():
    return """این ربات همزمان توی بله هم با قدرت فعال و در دسترسه! 🚀

اگه اونجا راحت‌تری، میتونی از طریق آیدی زیر پیداش کنی و دنگ‌هات رو اونجا مدیریت کنی:

🆔 @dong_yar_bot"""


def developer_info_message():
    return """سازنده‌ش ماییم! :) 🙋‍♂️️️️️️️️️️️️

من ایلیا اسماعیلی و هلیا قندی، دانشجو های مهندسی کامپیوتر(SBU) 🎓 

 دوتا نردِ عاشق هوش مصنوعی، برنامه‌نویسی و توسعه بک‌اند.

تو استک‌های مختلفی مثل پایتون، ++C، جاوا، فلاتر و... هم دست به کدیم و کلا از تبدیل کردن ایده‌ها به واقعیت لذت میبریم. ✨

اطلاعات بیشتر در گیتهاب من  : 
https://github.com/IliyaEsmaeili

اگه پروژه‌ای داشتی یا خواستی همکاری کنیم، با کمال میل هستیم! 🚀
راه‌های ارتباطی با ما:
📧 ایمیل کاری ایلیا: iliya.esmaeili.u@gmail.com
📧 ایمیل کاری هلیا: heliaghandi@mail.sbu.ac.ir
💼 لینکدین ایلیا: iliya-esmaeili
💼 لینکدین هلیا: helia-ghandi
"""

def bot_info_message():
   return """ایده ساخت این بات از یه درد مشترک و عمیق سرچشمه میگیره: دوستایی که هیچ‌وقت دنگ‌هاشون رو نمیزدن..! 🥲

 تصمیم گرفتیم دست به کد بشیم و این بات رو بنویسیم تا یه کمکی به مادر خرج های عزیز و مظلوم کرده باشیم.💳 😂

خلاصه که دوستانِ دنگ‌نده... دوران خوشی و فرار از دنگ به پایان رسید!
 یوهاهاها!😈(خودتون با لحن شیطانی بخونیدش)

برای دیدن کد بات روی دکمه "گیتهاب 💻" بزنید👇"""


def donate_info_message():
    return """حمایت مالی از این پروژه اصلا و ابدا اجباری نیست! 🙏

ولی اگه بات کارتو راه انداخت، تونستی دنگ‌هاتو زنده کنی و دوست داشتی ازمون حمایت کنی، میتونی یه قهوه مهمونمون کنی. ☕️

این حمایت‌ها مستقیما صرف نگهداری سرور، بهبود کیفیت همین بات و خلق پروژه‌های Open Source خفن‌ترِ بعدی میشه. دم همه‌تون گرم! ❤️

🔗 لینک حمایت مالی (دونیت):
https://reymit.ir/iliya_esmaeili"""


def dong_receipt_approval_message(dong_name, amount_per_person, receipt_sender_full_name, receipt_sender_user_name, receipt_sender_id, participants_list, group_name , unpaid_list) :
    if isinstance(participants_list, list):
        participants_text = "\n"
        for p in participants_list:
            if p in unpaid_list:
                participants_text = participants_text.__add__(f"  🔸 {p} | ❌ ").__add__("\n")
            else:
                participants_text = participants_text.__add__(f"  🔸 {p} | ✅ ").__add__("\n")
        # participants_text = "\n".join([ for p in participants_list])
    else:
        participants_text = participants_list

    return f"""💳 رسید جدید برای تأیید دنگ

🏷 نام دنگ: {dong_name} 
در گروه :‌{group_name}
💰 مبلغ سهم هر نفر: {amount_per_person} تومان
👤 ارسال‌کننده رسید: {receipt_sender_full_name if receipt_sender_full_name else "یافت نشد"}
@{receipt_sender_user_name if receipt_sender_user_name else "@ not found"}
🆔 شناسه کاربر: {receipt_sender_id}

👥 شرکت‌کنندگان دنگ:(و وضعیت پرداخت)
{participants_text}

━━━━━━━━━━━━━━

لطفاً مشخص کنید این پرداخت مربوط به کدام شرکت‌کننده است.

⚠️ پس از تأیید، وضعیت پرداخت فرد انتخاب‌شده در گروه اعلام خواهد شد."""

def bot_isnt_admin_message() :
    return "بات ادمین نیست"

def couldnt_pin_message() :
    return "دنگ فرستاده شد اما پین نشد!"

def bot_isnt_admin_and_couldnt_pin_message():
    return bot_isnt_admin_message() +"\n" + couldnt_pin_message()