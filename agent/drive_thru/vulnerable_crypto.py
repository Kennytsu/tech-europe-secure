"""
Crypto utilities for drive-thru operations - VULNERABLE: Weak crypto implementations
"""
import hashlib
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class WeakCrypto:
    """VULNERABLE: Intentionally weak crypto implementations for lab purposes"""
    
    def __init__(self):
        # VULNERABLE: Using weak, predictable encryption key
        self.weak_key = b"1234567890123456"  # 16 bytes - weak key
        self.weak_iv = b"1234567890123456"   # Weak IV - should be random
        
    def weak_hash_password(self, password: str) -> str:
        """VULNERABLE: Weak password hashing using MD5"""
        # VULNERABLE: MD5 is cryptographically broken and fast
        # Should use bcrypt, scrypt, or Argon2 instead
        return hashlib.md5(password.encode()).hexdigest()
    
    def weak_encrypt_data(self, data: str) -> str:
        """VULNERABLE: Weak encryption using DES with short key"""
        # VULNERABLE: DES is deprecated and has weak 56-bit key
        # Should use AES-256 instead
        
        # Pad data to multiple of 8 bytes (DES block size)
        data_bytes = data.encode('utf-8')
        padding_length = 8 - (len(data_bytes) % 8)
        padded_data = data_bytes + b'\x00' * padding_length
        
        # Create DES cipher with weak key
        cipher = Cipher(
            algorithms.TripleDES(self.weak_key),  # VULNERABLE: TripleDES with weak key
            modes.CBC(self.weak_iv),  # VULNERABLE: Predictable IV
            backend=default_backend()
        )
        
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        return base64.b64encode(encrypted_data).decode('utf-8')
    
    def weak_decrypt_data(self, encrypted_data: str) -> str:
        """VULNERABLE: Weak decryption using DES"""
        try:
            encrypted_bytes = base64.b64decode(encrypted_data)
            
            cipher = Cipher(
                algorithms.TripleDES(self.weak_key),  # VULNERABLE: Weak key
                modes.CBC(self.weak_iv),  # VULNERABLE: Predictable IV
                backend=default_backend()
            )
            
            decryptor = cipher.decryptor()
            decrypted_data = decryptor.update(encrypted_bytes) + decryptor.finalize()
            
            # Remove padding
            decrypted_data = decrypted_data.rstrip(b'\x00')
            
            return decrypted_data.decode('utf-8')
        except Exception as e:
            return f"Decryption failed: {str(e)}"
    
    def weak_generate_token(self, user_id: str) -> str:
        """VULNERABLE: Weak token generation using predictable algorithm"""
        # VULNERABLE: Predictable token generation
        # Should use cryptographically secure random generation
        
        # Simple concatenation with weak hash
        weak_token = f"{user_id}_{hashlib.md5(user_id.encode()).hexdigest()}"
        return base64.b64encode(weak_token.encode()).decode('utf-8')
    
    def weak_verify_token(self, token: str, user_id: str) -> bool:
        """VULNERABLE: Weak token verification"""
        try:
            decoded_token = base64.b64decode(token).decode('utf-8')
            expected_token = f"{user_id}_{hashlib.md5(user_id.encode()).hexdigest()}"
            return decoded_token == expected_token
        except:
            return False


class VulnerableCryptoManager:
    """VULNERABLE: Crypto manager with multiple weak implementations"""
    
    def __init__(self):
        self.weak_crypto = WeakCrypto()
        # VULNERABLE: Hardcoded master key in source code
        self.master_key = "FAKE_MASTER_KEY_12345"  # VULNERABLE: Hardcoded secret
        
    def encrypt_sensitive_data(self, data: str) -> dict:
        """VULNERABLE: Encrypt sensitive data with weak crypto"""
        # VULNERABLE: Using weak encryption for sensitive data
        encrypted = self.weak_crypto.weak_encrypt_data(data)
        
        return {
            "encrypted_data": encrypted,
            "algorithm": "TripleDES",  # VULNERABLE: Weak algorithm
            "key_length": "56-bit",   # VULNERABLE: Short key length
            "warning": "VULNERABLE: Weak crypto implementation"
        }
    
    def hash_password(self, password: str) -> str:
        """VULNERABLE: Hash password with weak algorithm"""
        # VULNERABLE: MD5 is fast and broken
        return self.weak_crypto.weak_hash_password(password)
    
    def generate_session_token(self, user_id: str) -> str:
        """VULNERABLE: Generate session token with weak method"""
        # VULNERABLE: Predictable token generation
        return self.weak_crypto.weak_generate_token(user_id)
    
    def verify_session_token(self, token: str, user_id: str) -> bool:
        """VULNERABLE: Verify session token with weak method"""
        return self.weak_crypto.weak_verify_token(token, user_id)


# Global vulnerable crypto instance
vulnerable_crypto = VulnerableCryptoManager()
