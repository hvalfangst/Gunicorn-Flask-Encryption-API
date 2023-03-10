import redis
from flask import request, jsonify
from datetime import datetime, timedelta
from functools import wraps
from crypto_utils import aes_decrypt
import jwt
import os

r = redis.Redis(host="localhost", port=6379, db=0)


def authenticate(username, password):
    encryption_key = os.environ.get("ENCRYPTION_KEY")

    # Check if the username key exists in the Redis cache
    if not r.exists(username):
        return False

    # Get the encrypted password associated with the given key username from Redis cache
    encrypted_password = r.get(username).decode("utf-8")

    # Decrypt the password
    decrypted_password = aes_decrypt(encryption_key, encrypted_password)

    # Check if the decrypted password matches the provided password
    return decrypted_password == password


def generate_jwt_token(username, encryption_key):
    payload = {
        "username": username,
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    # Encrypt payload with our key using HMAC-SHA
    token = jwt.encode(payload, encryption_key, algorithm="HS256")
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        encryption_key = os.environ.get("ENCRYPTION_KEY")
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Authorization header is missing"}), 401

        token = auth_header.split(" ")[1]

        try:
            jwt.decode(token, encryption_key, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.exceptions.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated
