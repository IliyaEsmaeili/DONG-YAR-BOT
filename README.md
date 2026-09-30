# Dongyar Bot (ربات دنگ یار)

<img src="./assets/new_logo_with_no_background.png" width="150" align="right" alt="Dongyar Avatar">

**Dongyar** is an open-source [Telegram](https://telegram.org/) bot for splitting group expenses (دنگ) in Persian chats.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![pyTelegramBotAPI](https://img.shields.io/pypi/v/pyTelegramBotAPI?label=pyTelegramBotAPI&logo=telegram&logoColor=white)](https://pypi.org/project/pyTelegramBotAPI/)
[![asyncpg](https://img.shields.io/pypi/v/asyncpg?label=asyncpg&logo=postgresql&logoColor=white)](https://pypi.org/project/asyncpg/)
[![python-dotenv](https://img.shields.io/pypi/v/python-dotenv?label=python-dotenv)](https://pypi.org/project/python-dotenv/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Release](https://img.shields.io/badge/release-v0.7.4%20beta-blue)](https://github.com/IliyaEsmaeili/DONG-YAR-BOT)

> [!NOTE]
> This project is currently a **Work In Progress (WIP)**. Many features are still under development!

> [!IMPORTANT]
> **Beta release.** `v0.7.4` is the first usable beta. Core flows work; expect rough edges before `v1.0.0`.

---

## What it does

- Starts a dong from a group or supergroup when someone types `دنگ`
- Walks the creator through a private setup wizard: name, amount, participants, notes, then confirm
- Lets the creator go back a step or cancel setup at any stage
- Stores users, dongs, and participants in PostgreSQL
- Posts a group summary with the per-person share and pins it when the bot is an admin
- Accepts payment receipts as replies to that summary (text, photo, or document)
- Detects common bank-transfer text and forwards receipts to the creator for approve / deny
- Marks payers as paid, updates the pinned summary, and keeps unpaid names available for the next receipt

---

## Requirements

- Python 3.10+
- PostgreSQL 15+
- A Telegram bot token from [@BotFather](https://t.me/BotFather)

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/IliyaEsmaeili/DONG-YAR-BOT.git
cd DONG-YAR-BOT
```

### 2. Install dependencies
first create your python venv then 
```bash
pip install pyTelegramBotAPI python-dotenv asyncpg
```

Use `pip3` on Unix-based systems if needed.

### 3. Environment variables (`.env`)

Create a `.env` file in the project root:

```bash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

DB_HOST=localhost
DB_PORT=5432
DB_NAME=dongyar
DB_USER_NAME=your_db_user
```


### 4. Set up PostgreSQL

Create an empty database, then load the schema:

```bash
cd src/database
python db_init.py
```

Use `python3` on Unix-based systems if needed. Run this from `src/database` so `schema.sql` resolves correctly.


Do not put spaces around `=`. Do not commit this file.

### 5. Run the bot

From the `src/` directory:

```bash
cd src
python bot_main.py
```

Use `python3` on Unix-based systems if needed.

Add the bot to your Telegram group. Grant it admin rights if you want summary messages pinned.

---

## Usage

1. Add the bot to a group (or start it in private with `/start`).
2. In the group, type `دنگ`.
3. Tap **ایجاد دنگ جدید** and finish the steps in a private chat with the bot.
4. The bot posts (and pins, if allowed) a summary in the group.
5. Participants reply to that message with a receipt (text or image).
6. The creator approves or denies the payment from their private chat.

---

## Project structure

```
└── src
    ├── bot_instance.py
    ├── bot_main.py
    ├── data.py
    ├── database
    │   ├── connection.py
    │   ├── db_init.py
    │   ├── repositories.py
    │   └── schema.sql
    ├── dong_handler.py
    ├── keyboards.py
    ├── message_template.py
    ├── stage_blue_prints.py
    └── util
        ├── receipt_detector.py
        └── stage_util.py
```

---

## Roadmap

- Reminder tones (friendly, strict, and similar styles)
- Image / OCR receipt parsing (photos are forwarded today, not parsed)
- Clearer payment status views
- Hardening, tests, and a pinned `requirements.txt` toward `v1.0.0`

---

## Contributing

Issues and pull requests are welcome. See [SECURITY.md](SECURITY.md) for vulnerability reporting.

---

## License

MIT — see [LICENSE](LICENSE).
