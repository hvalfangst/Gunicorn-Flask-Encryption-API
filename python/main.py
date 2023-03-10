from flask import Flask, jsonify
from crypto_utils import aes_encrypt, aes_decrypt
from env_utils import get_body, get_credentials
from security_utils import token_required, authenticate, generate_jwt_token
import redis
import os

app = Flask(__name__)
r = redis.Redis(host="localhost", port=6379, db=0)


@app.route("/encrypt", methods=["POST"])
@token_required
def encrypt():
    encryption_key, pod_name, text = get_body()
    encrypted_text = aes_encrypt(encryption_key, text)

    response = {
        "pod_name": pod_name,
        "encrypted_text": encrypted_text
    }

    return jsonify(response)


@app.route("/decrypt", methods=["POST"])
@token_required
def decrypt():
    encryption_key, pod_name, text = get_body()
    decrypted_ciphertext = aes_decrypt(encryption_key, text)

    response = {
        "pod_name": pod_name,
        "decrypted_cipher": decrypted_ciphertext
    }

    return jsonify(response)


@app.route("/login", methods=["POST"])
def login():
    encryption_key, password, username = get_credentials()

    # Check if the username and password are provided
    if not (username and password):
        return jsonify({"error": "Username or password is missing"})

    # Generate token if the supplied username/password pair exists in our redis cache
    if authenticate(username, password):
        token = generate_jwt_token(username, encryption_key)
        return jsonify({"token": token})
    else:
        return jsonify({"error": "Invalid username or password"})


@app.route("/users", methods=["GET"])
def get_users():
    # Retrieve all keys
    keys = r.keys('*')

    # Retrieve all data
    data = r.mget(keys)

    # Convert data to dictionary
    result = {}
    for key, value in zip(keys, data):
        result[key.decode("utf-8")] = value.decode("utf-8")

    # Return JSON response
    return jsonify(result)


@app.route("/users", methods=["POST"])
def create_user():
    encryption_key, password, username = get_credentials()

    # Check if the username and password are provided
    if not (username and password):
        return jsonify({"error": "Username or password is missing"})

    # Encrypt the password using our encryption key
    encrypted_password = aes_encrypt(encryption_key, password)

    # Set value associated with key username to be the encrypted password
    r.set(username, encrypted_password)

    # Return JSON response
    return jsonify({"message": f"Credentials associated with user {username} has been created"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
