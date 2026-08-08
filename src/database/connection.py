import asyncpg
import os
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER_NAME = os.getenv("DB_USER_NAME")
pool = None


async def create_pool():
    global pool

    pool = await asyncpg.create_pool(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER_NAME,
        min_size=1,
        max_size=10
    )


def get_pool():
    return pool