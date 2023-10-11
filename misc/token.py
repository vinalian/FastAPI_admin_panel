from database.basemodels import UserSchema
import jwt
from dotenv import load_dotenv
from os import environ

load_dotenv()


def create_jwt_token(user: UserSchema):
    encoded_jwt = jwt.encode({"username": user.login}, environ.get('SECRET_TOKEN'), algorithm="HS256")
    return encoded_jwt


def decode_jwt_token(token: str):
    decoded_jwt = jwt.decode(token,  environ.get('SECRET_TOKEN'), algorithms=["HS256"])
    return decoded_jwt


def validate_token(token: str) -> dict or None:
    try:
        decoded_jwt = decode_jwt_token(token)
        if decoded_jwt.get('username'):
            return decoded_jwt
    except:
        return False
