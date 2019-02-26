import jwt
import datetime
import bcrypt
from sanic import response
import functools



def create_auth_token(user_id, secret):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            secret,
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_token(auth_token, secret):

    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
        """
    try:
        payload = jwt.decode(auth_token, secret)
        resp =  {
            'status': 'success',
            'user_id': payload['sub']
        }
    except jwt.ExpiredSignatureError:
        resp =  {
            'status': 'error',
            'message': 'Signature expired. Please log in again.'
        }
    except jwt.InvalidTokenError:
        resp =  {
            'status': 'error',
            'message': 'Invalid token. Please log in again.'
        }

    return resp



def check_token(f):
    async def wrapper(*args, **kwargs):
        req = args[0]
        token = req.args.get("token")
        if token:
            decoded = decode_token(token, req.app.config["SECRET"])
            if decoded["status"] != "success":
                resp = response.json(decoded)
            else:
                resp = await f(*args, **kwargs)
        else:
            resp = response.json({"status": "error", "message": "not allowed"})
        return resp
    return wrapper


def hash_passwd(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def check_passwd(plain_pass, hash_pass):
    return bcrypt.checkpw(plain_pass.encode("utf-8"), hash_pass.encode("utf-8"))

def create_jwt(data, secret, algorithm="HS256"):
    return jwt.encode(data, secret, algorithm)

def decode_jwt(token, secret):
    try:
        return jwt.decode(token, secret)
    except jwt.InvalidTokenError:
        return None




def login_required(f):
    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        req = args[0]
        if req.json.get("token") and decode_jwt(req.json.get("token")):
            async with req.app.redis.get() as redis:
                token = await redis.get(req.json.get("token"))
                if not token:
                    return await f(*args, **kwargs)
        return response.json({"status": "error", "message": "invalid token"})
    return wrapper

def token_required(f):
    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        req = args[0]
        if req.headers.get("BB-KEY") == req.app.config.get("API_KEY"):
           return await f(*args, **kwargs)
        return response.json({"status": "error", "message": "invalid token"})
    return wrapper

