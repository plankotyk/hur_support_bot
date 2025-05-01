from contextlib import asynccontextmanager

import asyncpg
import logging
from config.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from bot.dtos.appeal_dto import AppealDTO


logger = logging.getLogger(__name__)


_pool = None

async def get_pool():
    global _pool
    if _pool is None:
        try:
            _pool = await asyncpg.create_pool(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                min_size=1,
                max_size=10
            )
            logger.info("Database connection pool initialized successfully")
        except asyncpg.exceptions.PostgresError as e:
            logger.error(f"Failed to initialize database pool: {e}")
            raise
    return _pool

async def close_pool():
    global _pool
    if _pool is not None:
        try:
            await _pool.close()
            logger.info("Database connection pool closed successfully")
        except asyncpg.exceptions.PostgresError as e:
            logger.error(f"Failed to close database pool: {e}")
            raise
        finally:
            _pool = None

@asynccontextmanager
async def get_connection():
    pool = await get_pool()
    conn = await pool.acquire()
    try:
        yield conn
    except asyncpg.exceptions.PostgresError as e:
        logger.error(f"Database operation error: {e}")
        raise
    finally:
        await pool.release(conn)


async def init_db():
    async with get_connection() as conn:
        async with conn.transaction():
            try:
                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS appeals (
                        id TEXT PRIMARY KEY,
                        user_id BIGINT,
                        username TEXT,
                        profile_link TEXT,
                        direction TEXT,
                        message TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                await conn.execute('''
                   CREATE TABLE IF NOT EXISTS donation_settings (
                       key TEXT PRIMARY KEY,
                       value TEXT NOT NULL
                   )
                ''')

                await conn.execute('''
                   INSERT INTO donation_settings (key, value)
                   VALUES ($1, $2) ON CONFLICT (key) DO NOTHING
                   ''', 'donation_message', 'Наразі триває збір на безпілотні комплекси "Рись" для ПАД Кракен:\n\n'
                )

                await conn.execute('''
                   INSERT INTO donation_settings (key, value)
                   VALUES ($1, $2) ON CONFLICT (key) DO NOTHING
                   ''', 'donation_link', 'https://send.monobank.ua/jar/3dh33n2YpP'
                )

                logger.info("Successfully initialized database.")
            except asyncpg.exceptions.PostgresError as e:
                logger.error(f"Failed to initialize database: {e}")
                raise


async def get_value_by_key(key: str):
    async with get_connection() as conn:
        try:
            result = await conn.fetchrow(
                'SELECT value FROM donation_settings WHERE key = $1', key
            )
            value = result['value'] if result else ''
            logger.info("Successfully returned value by key.")
            return value
        except asyncpg.exceptions.PostgresError as e:
            logger.error(f"Failed to return value by key: {e}")
            raise


async def update_value_by_key(key: str, value: str):
    async with get_connection() as conn:
        try:
            await conn.execute('''
               INSERT INTO donation_settings (key, value)
               VALUES ($1, $2) ON CONFLICT (key) DO
               UPDATE
                   SET value = EXCLUDED.value
               ''', key, value
            )
            logger.info("Successfully updated value by key.")
        except asyncpg.exceptions.PostgresError as e:
            logger.error(f"Failed to update value by key: {e}")
            raise


async def save_appeal(appeal: AppealDTO):
    async with get_connection() as conn:
        try:
            await conn.execute(
                '''
                INSERT INTO appeals (id, user_id, username, profile_link, direction, message, created_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                ''',
                appeal.id, appeal.user_id, appeal.username, appeal.profile_link,
                appeal.direction, appeal.message, appeal.created_at
            )
            logger.info("Successfully saved appeal.")
        except asyncpg.exceptions.PostgresError as e:
            logger.error(f"Failed to save appeal: {e}")
            raise


async def get_all_appeals():
    async with get_connection() as conn:
        try:
            appeals_records = await conn.fetch(
                'SELECT * FROM appeals ORDER BY created_at DESC'
            )
            appeals = [AppealDTO(**dict(record)) for record in appeals_records]
            logger.info("Successfully fetched all appeals.")
            return appeals
        except asyncpg.exceptions.PostgresError as e:
            logger.error(f"Failed to fetch all appeals: {e}")
            raise


async def get_last_10_appeals():
    async with get_connection() as conn:
        try:
            appeals_records = await conn.fetch(
                'SELECT * FROM appeals ORDER BY created_at DESC LIMIT 10'
            )
            appeals = [AppealDTO(**dict(record)) for record in appeals_records]
            logger.info("Successfully fetched last 10 appeals.")
            return appeals
        except asyncpg.exceptions.PostgresError as e:
            logger.error(f"Failed to fetch last 10 appeals: {e}")
            raise