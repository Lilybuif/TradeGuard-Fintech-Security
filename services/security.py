from cryptography.fernet import Fernet
import os

KEY_FILE = "secret.key"

def load_or_create_key() -> bytes:
    """Loads an existing encryption key or generates a new one if it doesn't exist."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key

# Initialize the cipher suite with our secret key
ENCRYPTION_KEY = load_or_create_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

def encrypt_api_key(plain_api_key: str) -> str:
    """Encrypts a plaintext financial API key into secure ciphertext."""
    encrypted_bytes = cipher_suite.encrypt(plain_api_key.encode("utf-8"))
    return encrypted_bytes.decode("utf-8")

def decrypt_api_key(encrypted_api_key: str) -> str:
    """Decrypts a ciphertext string back into the original plaintext API key."""
    decrypted_bytes = cipher_suite.decrypt(encrypted_api_key.encode("utf-8"))
    return decrypted_bytes.decode("utf-8")

if __name__ == "__main__":
    # Quick local test of the security module
    test_key = "secret_brokerage_api_key_12345"
    encrypted = encrypt_api_key(test_key)
    decrypted = decrypt_api_key(encrypted)
    print(f"Original: {test_key}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")