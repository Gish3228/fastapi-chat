from argon2 import PasswordHasher
from datetime import datetime, timezone, timedelta
import jwt

from ..config import JWTSettings


password_hasher = PasswordHasher()


def get_password_hash(password):
    return password_hasher.hash(password)


def verify_password(plain_password, hashed_password):
    return password_hasher.verify(plain_password, hashed_password)


def create_access_token(data: dict, jwt_settings: JWTSettings):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=jwt_settings.token_expire_days)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwt_settings.secret_key, algorithm=jwt_settings.algorithm)
    return encoded_jwt
