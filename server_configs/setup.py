import os
import uvloop
import asyncio
import json
import asyncpg
from loguru import logger

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

running_loop = asyncio.get_event_loop()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


async def create_pool(uri, **kwargs):
    """Creates a connection pool to the specified PostgreSQL server"""

    def _encode_jsonb(value):
        return b'\x01' + json.dumps(value).encode('utf-8')

    def _decode_jsonb(value):
        return json.loads(value[1:].decode('utf-8'))

    async def init(con):
        await con.set_type_codec('jsonb', schema='pg_catalog', encoder=_encode_jsonb, decoder=_decode_jsonb,
                                 format="binary")

    try:
        logger.debug("Creating database connection pool")

        return await asyncpg.create_pool(uri, init=init, **kwargs)
    except ValueError:
        logger.error("PostgreSQL error: Invalid URI, check postgresql.txt. "
                     "Format must be 'postresql://user:password@host/database'")
    except asyncpg.PostgresError as e:
        logger.error(f"PostgreSQL error: {e}")
    except TimeoutError:
        logger.error("PostgreSQL error: Connection timed out.")
    except Exception as e:
        logger.error(f"Unexpected error: {e.__class__.__name__}: {e}")


db_pool = running_loop.create_task(create_pool(DATABASE_URI, min_size=10, max_size=30))
