# Dongyar Bot (ربات دنگ یار)

<img src="./assets/new_logo_with_no_background.png" width="150" align="right" alt="Dongyar Avatar">

**Dongyar** is an open-source bot for [Telegram](https://telegram.org/) designed to make bill splitting and group expense management easy.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![pyTelegramBotAPI](https://img.shields.io/pypi/v/pyTelegramBotAPI?label=pyTelegramBotAPI&logo=telegram&logoColor=white)](https://pypi.org/project/pyTelegramBotAPI/)
[![asyncpg](https://img.shields.io/pypi/v/asyncpg?label=asyncpg&logo=postgresql&logoColor=white)](https://pypi.org/project/asyncpg/)
[![python-dotenv](https://img.shields.io/pypi/v/python-dotenv?label=python-dotenv)](https://pypi.org/project/python-dotenv/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-WIP-orange)](https://github.com/IliyaEsmaeili/DONG-YAR-BOT)

> [!NOTE]
> This project is currently a **Work In Progress (WIP)**. Many features are still under development!

> [!IMPORTANT]
> This project is currently in pre-release (prior to v1.0.0). It is not yet stable or production-ready, and you may encounter bugs.

---

## Features

**Currently implemented:**

- Group trigger on the word `دنگ` with inline setup keyboard
- Full private-chat dong creation wizard (name, amount, participants, notes, confirm)
- PostgreSQL persistence for users, dongs, and participants
- Pinned group summary message per dong with paid/unpaid tracking
- Receipt submission via reply (text, photo, or document) to the pinned summary
- Heuristic receipt text detection for bank transfer messages
- Creator approval flow with inline buttons (approve payer / deny payment)
- Live group updates when a payment is approved (summary edit, pin/unpin fallback)
- Private `/start` menu with usage guide, GitHub info, and bot metadata

**Planned / In Development:**

- **Custom Tones:** Remind users to pay in different personas (Friendly, Strict, Literary, etc.)
- **Smarter receipt handling:** OCR / image-based receipt parsing (photos are forwarded today, but not parsed)
- **Status reports:** Richer dashboards for who paid, who did not, and total collected
- **Stability & v1.0.0:** Hardening, tests, and a proper `requirements.txt`

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/IliyaEsmaeili/DONG-YAR-BOT.git
cd DONG-YAR-BOT
```

### 2. Install dependencies

Make sure you have Python 3.10+ installed. Then run:

```bash
pip install pyTelegramBotAPI python-dotenv asyncpg
```

*(Use `pip3` on Unix-based systems.)*

### 3. Set up PostgreSQL

Create a database, then initialize the schema:

```bash
cd src/database
python db_init.py
```

*(Use `python3` on Unix-based systems. Run this from `src/database` so `schema.sql` resolves correctly.)*

### 4. Environment variables (`.env`)

Create a `.env` file in the project root:

```bash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

DB_HOST=localhost
DB_PORT=5432
DB_NAME=dongyar
DB_USER_NAME=your_db_user
```

*(Do not put spaces around the `=` sign. Do not commit this file.)*

### 5. Run the bot

From the `src/` directory:

```bash
cd src
python bot_main.py
```

*(Use `python3` on Unix-based systems.)*

The bot must be added to your Telegram group and granted admin rights if you want it to pin dong summary messages.

---

## Usage (quick overview)

1. Add the bot to a group and type `دنگ`.
2. The group admin (مادرخرج) taps **ایجاد دنگ جدید**.
3. Complete the setup steps in a private chat with the bot.
4. The bot posts and pins a summary in the group.
5. Participants reply to that message with their receipt (text or image).
6. The creator approves or denies the payment from their private chat.

---

## Project structure

```
src/
├── bot_main.py           # Entry point, handlers, receipt flow
├── bot_instance.py       # AsyncTeleBot setup
├── dong_handler.py       # Start dong creation from group
├── stage_blue_prints.py  # Multi-step dong creation stages
├── keyboards.py          # Reply & inline keyboards
├── message_template.py   # Persian message templates
├── data.py               # User / Dong models
├── database/
│   ├── connection.py     # asyncpg pool
│   ├── repositories.py   # DB queries
│   ├── schema.sql        # Tables
│   └── db_init.py        # One-time schema setup
└── util/
    └── receipt_detector.py
```

---

## Contributing

Issues and pull requests are welcome. See [SECURITY.md](SECURITY.md) for vulnerability reporting.

---

## License

MIT — see [LICENSE](LICENSE).


