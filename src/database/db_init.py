import asyncio

from connection import create_pool , get_pool


from pathlib import Path


async def start_db_and_create_table_schema():
    await create_pool()
    pool = get_pool()
    async with pool.acquire() as conn:
        await conn.execute(Path("schema.sql").read_text())


asyncio.run(start_db_and_create_table_schema())


