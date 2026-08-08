from .connection import get_pool
from data import User , Dong

async def execute_query(query, *params):
    pool = get_pool()
    async with pool.acquire() as conn:
        await conn.execute(query, *params)


async def fetch_one(query, *params):
    pool = get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, *params)


async def fetch_all(query, *params):
    pool = get_pool()
    async with pool.acquire() as conn:
        return await conn.fetch(query, *params)


async def save_user(user):
    pool = get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO users
            (telegram_id, full_name)
            VALUES ($1, $2)
                ON CONFLICT DO NOTHING
            """,
            user.telegram_id,
            user.full_name
        )


async def save_dong(dong):
    pool = get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO dongs
            (group_id, creator_id)
            VALUES ($1, $2)
            """,
            dong.group_id,
            dong.creator_id
        )

async def user_state_fetch(message):
    telegram_id = message.from_user.id

    row = await fetch_one(
        """
        SELECT *
        FROM users
        WHERE telegram_id = $1
        """,
        telegram_id
    )

    if row is None:
        return None

    return row["state"]

async def change_user_state(user, state):
    await execute_query(
        """
        UPDATE users
        SET state = $1
        WHERE telegram_id = $2
        """,
        state,
        user.id
    )


async def get_user_from_telegram_id(telegram_id):
    row = await fetch_one(
        """SELECT * FROM users WHERE telegram_id = $1
        """,
        telegram_id)
    if row is None:
        return None

    user = User(telegram_id=row["telegram_id"],full_name=row["full_name"],state=row["state"]
    )
    user.dong = []
    dongs = await fetch_all(
        """SELECT * FROM dongs WHERE creator_id = $1
        """,
        telegram_id)

    for dong_row in dongs:
        dong = Dong(
            dong_id=dong_row["id"],
            name=dong_row["name"],
            amount=dong_row["amount"],
            additional_info=dong_row["additional_info"],
            big_prompt_message=dong_row["big_prompt_message"],
            group_id=dong_row["group_id"],
            creator_id=dong_row["creator_id"]
        )

        participants = await fetch_all(
            """SELECT * FROM dong_participants WHERE dong_id = $1
            """,
            dong.local_dong_id
        )

        dong.participants = [
            participant["user_name"]
            for participant in participants
        ]

        user.dong.append(dong)

    return user