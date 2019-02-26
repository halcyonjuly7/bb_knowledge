from . import accounts
from psycopg2 import sql

from sanic import response
from core.db.models import Accounts
from core.security import check_passwd, hash_passwd, decode_jwt, create_jwt, token_required, login_required
import jwt



@accounts.route("/login", methods=["POST"])
@token_required
async def login(request):
    async with request.app.pg.get_cursor() as cur:
        await cur.execute(sql.SQL(
            "SELECT {0},{1} FROM {2} WHERE {3} = %s"
        ).format(sql.Identifier(Accounts.UUID),
                 sql.Identifier(Accounts.PASSWORD),
                 sql.Identifier(Accounts.TABLE_NAME),
                 sql.Identifier(Accounts.EMAIL)),
                [request.json.get("email")])
        user = await cur.fetchone()
        if user:
            if check_passwd(request.json.get("password"), user[Accounts.PASSWORD]):
                return response.json({"status": "success",
                        "token": create_jwt(user, request.app.config["SECRET"])})
            return response.json({"status": "error", "message": "invalid password"})
        return response.json({"status": "error", "message": "unknown user"})




@accounts.route("/logout", methods=["POST"])
@login_required
@token_required
async def logout(request):
    async with request.app.redis.get() as redis:
        pipeline = redis.pipeline()
        pipeline.set(request.json.get("token"), "")
        pipeline.setex(request.json.get("token"), request.app.config["TOKEN_EXPIRATION"])
        await pipeline.execute()
        return response.json({"status": "success", "message": "user logged out"})
    return response.json({"status": "error"})


@accounts.route("/signup", methods=["POST"])
@token_required
async def signup(request):

    async with request.app.pg.get_cursor() as cur:
        await cur.execute(sql.SQL("""
        SELECT {0} FROM {1} WHERE {2} = %s;
        """).format(sql.Identifier(Accounts.EMAIL),
                    sql.Identifier(Accounts.TABLE_NAME),
                    sql.Identifier(Accounts.EMAIL)),
               [request.json.get("email")])

        user = await cur.fetchone()
        if user is None:
            await cur.execute(sql.SQL(
                "INSERT INTO {0} ({1}, {2}, {3}, {4}) VALUES (%s, %s, %s, %s);"
            ).format(sql.Identifier(Accounts.TABLE_NAME),
                     sql.Identifier(Accounts.FIRST_NAME),
                     sql.Identifier(Accounts.LAST_NAME),
                     sql.Identifier(Accounts.PASSWORD),
                     sql.Identifier(Accounts.EMAIL)),
            [request.json.get("first_name"),
             request.json.get("last_name"),
             hash_passwd(request.json.get("password")).decode("utf-8"),
             request.json.get("email")])
            return response.json({"status": "success"})
        return response.json({"status": "error", "message": "email in use"})



@accounts.route("/all", methods=["GET"])
@token_required
async def get_accounts(request):
    async with request.app.pg.get_cursor() as cur:
        cur.execute(sql.SQL("""
        SELECT
        """))

@accounts.route("/oauth/<provider>", methods=["POST"])
async def oath_signup(request, provider):
    pass