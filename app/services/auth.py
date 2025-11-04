import secrets
from datetime import UTC, datetime, timedelta
from typing import Any, Dict

import jwt
import jwt.exceptions
import jwt.utils
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from app.settings import settings


def hash_password(password: str) -> tuple[bytes, bytes]:
    salt = secrets.token_bytes(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    hashed = kdf.derive(password.encode())
    return (hashed, salt)


def verify_password(password: str, stored_hash: bytes, salt: bytes) -> bool:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    try:
        kdf.verify(password.encode(), stored_hash)
        return True
    except Exception:
        return False


def create_access_token(
    payload: dict, expires_delta: timedelta = timedelta(days=1)
) -> tuple[str, str]:
    secret = secrets.token_urlsafe(64)
    expire = datetime.now(UTC) + expires_delta
    payload["expire"] = expire.ctime()
    payload["secret"] = secret
    token = jwt.JWT().encode(
        payload, jwt.jwk.OctetJWK(settings.JWT_SECRET_KEY.encode())
    )
    return token, secret


def decode_access_token(token: str) -> Dict[str, Any] | None:
    try:
        decoded_token: dict = jwt.JWT().decode(
            token,
            jwt.jwk.OctetJWK(settings.JWT_SECRET_KEY.encode()),
            algorithms=["HS256"],
        )
    except jwt.exceptions.JWTDecodeError:
        return None
    return decoded_token
