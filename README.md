# 💸 Dongyar Bot (ربات دنگ یار)

<img src="./assets/profile_picture.png" width="120" align="right" alt="Dongyar Avatar">

**Dongyar** is an open-source bot for [Bale](https://bale.ai/) and [Telegram](https://telegram.org/) designed to make bill splitting and group expense management incredibly easy. 

> [!NOTE]
> This project is currently a **Work In Progress (WIP)**. Many features are still under development!

---

## 🌟 Features 
**Currently implemented:**
- Responds to group triggers (like "دنگ").
- Basic setup and inline keyboard routing.

**Planned / In Development:**
- 📝 **Set Mother-Spender (Madar Kharj):** Enter card details, total amount, and specific payers.
- 🎭 **Custom Tones:** The bot will remind users to pay in different personas (Friendly, Strict, Literary, etc.).
- 🧾 **Receipt Verification:** Users send their payment receipts, and the bot updates the remaining balance.
- 📊 **Status Reports:** See exactly who has paid, who hasn't, and how much money is collected.

---

## 🚀 Installation & Setup 

### 1. Clone the repository
```bash
git clone [repository_url]
cd DONG-YAR-BOT
```

### 2. Install dependencies

Make sure you have Python installed. Then run:
```bash
pip install pyTelegramBotAPI python-dotenv
```
*(**Note:** Use `pip3` on Unix-based OS)*

### 3. Environment Variables (.env)
Create a `.env` file in the root directory and add your bot token. By default, the code looks for a Bale Bot Token:  
  *(put this line in your `.env` file)*
```bash
BALE_BOT_TOKEN=your_bale_bot_token_here
```
*(**Note:** Do not put spaces around the `=` sign)*

### 4. Running for Bale vs. Telegram

**For Bale Messenger (بله):**
The code is currently configured for Bale by default  
(due to development network constraints, Telegram will be the default upon completion). Just run:  
```bash
python bot_main.py
```
*(**Note:** Use `python3` on Unix-based OS)*

**For Telegram (تلگرام):**
If you want to use this bot on Telegram instead of Bale:
1. Change the variable name in your `.env` file to `TELEGRAM_BOT_TOKEN` (optional, but recommended for clarity).
2. Update the Python code to load the new variable name.
3. **Crucial:** Remove or comment out this line in your code, as it redirects requests to Bale's API:

### 5. ⚠️Remove this line(on bale.py) for Telegram use!⚠️
```python
apihelper.API_URL = "https://tapi.bale.ai/bot{0}/{1}"
```
