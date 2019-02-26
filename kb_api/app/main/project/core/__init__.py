import aioredis
import os
from sanic import Sanic

def app_factory():
    app = Sanic()
    # app.config.from_pyfile(conf)
    from .db import DbHelper
    conf_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "conf", "dev.py")
    app.config.from_pyfile(conf_path)

    from .blueprints import accounts
    from .blueprints import questions

    app.blueprint(accounts, url_prefix="/account")
    app.blueprint(questions, url_prefix="/questions")

    @app.listener('before_server_start')
    async def setup(app, loop):
        # POSTGRES SETUP
        app.pg = DbHelper()
        pg_conf = app.config['DB_CONF']['POSTGRES']
        conn = f"postgres://{pg_conf['PG_USER']}:{pg_conf['PG_PASS']}@postgres/{pg_conf['PG_DB']}"
        await app.pg.init_conn(conn)
        await app.pg.init_db()

        # REDIS SETUP
        app.redis = await aioredis.create_pool(
            ('redis', 6379),
            minsize=5,
            maxsize=10,
            loop=loop
    )

    @app.listener("before_server_stop")
    async def teardown(app, loop):
        # POSTGRES TEARDOWN
        await app.pg.teardown_db()

        #REDIS TEARDOWN
        app.redis.close()
        await app.redis.wait_closed()

    return app