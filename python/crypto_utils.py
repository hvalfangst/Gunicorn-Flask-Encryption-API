from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
import base64


def base64_encode(input_bytes: bytes) -> str:
    return base64.b64encode(input_bytes).decode("utf-8")


def base64_decode(input_str: str) -> bytes:
    return base64.b64decode(input_str.encode("utf-8"))


def generate_salt_32_byte() -> bytes:
    return get_random_bytes(32)


def aes_encrypt(encryption_key: str, plaintext: str) -> str:
    # Convert plaintext encryption key to bytes
    password_bytes = encryption_key.encode("ascii")
    # Generate random sequence of 32 bytes
    salt = generate_salt_32_byte()
    # Set key derivation interation count to 15000
    pbkdf2_iterations = 15000

    # Derive new key based on encryption key, salt and iterations
    derived_key = PBKDF2(
        password_bytes, salt, 32, count=pbkdf2_iterations, hmac_hash_module=SHA256
    )

    cipher = AES.new(derived_key, AES.MODE_CBC)

    # Encrypt plaintext using our CBC cipher
    ciphertext = cipher.encrypt(pad(plaintext.encode("ascii"), AES.block_size))

    # B64-encode iv, salt and ciphertext (from bytes to text)
    iv_base64 = base64_encode(cipher.iv)
    salt_base64 = base64_encode(salt)
    ciphertext_base64 = base64_encode(ciphertext)

    # Return tuple containing base64-encoded {salt, iv and ciphertext}
    return f"{salt_base64}:{iv_base64}:{ciphertext_base64}"


def aes_decrypt(encryption_key: str, ciphertext_base64: str) -> str:
    # Convert plaintext encryption key to bytes
    password_bytes = encryption_key.encode("ascii")

    # B64-decode tuple containing ciphertext, salt and iv (from text to bytes)
    data = ciphertext_base64.split(":")
    salt = base64_decode(data[0])
    iv = base64_decode(data[1])
    ciphertext = base64_decode(data[2])

    # Set key derivation interation count to 15000
    pbkdf2_iterations = 15000

    # Derive new key based on encryption key, salt and iterations
    derived_key = PBKDF2(
        password_bytes, salt, 32, count=pbkdf2_iterations, hmac_hash_module=SHA256
    )

    cipher = AES.new(derived_key, AES.MODE_CBC, iv)

    # Decrypt ciphertext using derived_key key and iv
    decrypted_text = unpad(cipher.decrypt(ciphertext), AES.block_size)

    # Return original plain text as text
    return decrypted_text.decode("utf-8")
