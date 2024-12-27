import jwt
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import padding, serialization
from cryptography.hazmat.primitives import hashes
from app.config.settings import SECRET_KEY, ALGORITHM, JWT_EXPIRES_IN_MINUTES


def create_jwt(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=JWT_EXPIRES_IN_MINUTES)
    payload["iat"] = datetime.utcnow()
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_jwt(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Token invalid


def verify_signature(public_key_pem, challenge, signed_challenge):
    public_key = serialization.load_pem_public_key(public_key_pem.encode())
    try:
        public_key.verify(
            bytes.fromhex(signed_challenge),
            challenge.encode(),
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
        return True
    except Exception:
        return False
