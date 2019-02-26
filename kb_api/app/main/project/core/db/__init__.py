import psycopg2
import aiopg

from contextlib import asynccontextmanager
from psycopg2 import sql
from .models import create_models
from .associations import create_associations




class DbHelper:
    def __init__(self):
        self._conn = None


    async def init_conn(self, conn):
        self._conn = await aiopg.connect(conn)

    async def init_db(self):
        async with self.get_cursor() as cur:
            await create_models(cur)
            await create_associations(cur)

    async def teardown_db(self):
        await self._conn.close()

    @asynccontextmanager
    async def get_cursor(self):
        try:
            cur = await self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            yield cur
        finally:
            cur.close()








