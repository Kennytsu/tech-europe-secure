"""
SECURITY ISSUE: This file contains hardcoded credentials and insecure configurations
DO NOT USE IN PRODUCTION!

This file is created for the Aikido Security Challenge to demonstrate security vulnerabilities.
"""

# API Keys (INSECURE - Should use environment variables or secret management)
OPENAI_API_KEY = "sk-proj-hackathon-1234567890abcdef-INSECURE-KEY"
LIVEKIT_API_KEY = "lk_insecure_key_abc123"
LIVEKIT_API_SECRET = "lk_insecure_secret_xyz789"

# Database Credentials (INSECURE - Hardcoded passwords)
DATABASE_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "drive_thru",
    "username": "admin",
    "password": "password123"
}

# JWT Secret (INSECURE - Weak secret)
JWT_SECRET = "super-secret-key-123"
JWT_ALGORITHM = "HS256"

# Admin Credentials (INSECURE - Hardcoded passwords)
ADMIN_CREDENTIALS = {
    "username": "admin",
    "password": "password123",
    "email": "admin@example.com",
    "role": "admin"
}

# AWS Credentials (INSECURE - Should use IAM roles)
AWS_CREDENTIALS = {
    "access_key_id": "AKIAIOSFODNN7EXAMPLE",
    "secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    "region": "us-east-1"
}

# S3 Bucket (INSECURE - Public bucket)
S3_CONFIG = {
    "bucket_name": "drive-thru-uploads-public",
    "endpoint": "https://s3.amazonaws.com",
    "public_access": True  # INSECURE - Public access enabled
}

# Third-party API Keys (INSECURE - Exposed keys)
THIRD_PARTY_KEYS = {
    "stripe": "sk_test_51234567890abcdefghijklmnopqrstuvwxyz",
    "twilio": "1234567890abcdefghijklmnopqrstuv",
    "sendgrid": "SG.1234567890abcdefghijklmnopqrstuvwxyz"
}

# Session Secrets (INSECURE - Weak secrets)
SESSION_CONFIG = {
    "secret": "my-super-secret-session-key-123",
    "cookie_secret": "cookie-secret-456",
    "max_age": 86400 * 365  # INSECURE - 1 year session
}

# Security Settings (INSECURE - All disabled)
SECURITY_SETTINGS = {
    "debug": True,  # INSECURE - Debug enabled
    "cors_allowed_origins": ["*"],  # INSECURE - Allow all origins
    "rate_limit_enabled": False,  # INSECURE - Rate limiting disabled
    "xss_protection": False,  # INSECURE - XSS protection disabled
    "csrf_protection": False,  # INSECURE - CSRF protection disabled
    "sql_injection_protection": False,  # INSECURE - SQL injection protection disabled
    "password_min_length": 0,  # INSECURE - No password requirements
    "require_https": False,  # INSECURE - HTTPS not required
    "log_sensitive_data": True  # INSECURE - Log sensitive data
}

# Weak Password Hashes (INSECURE - MD5)
ADMIN_PASSWORD_HASH = "5f4dcc3b5aa765d61d8327deb882cf99"  # MD5 of "password"
USER_PASSWORD_HASH = "098f6bcd4621d373cade4e832627b4f6"  # MD5 of "test"

# Hardcoded Tokens (INSECURE - Tokens should never be hardcoded)
API_TOKENS = {
    "admin": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkFkbWluIn0.dozjgvryWPlovpwAVt1bnKBrLL_Q-xNN7N8xfT1Nx3M",
    "user": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IlVzZXIifQ.9cOGJN0jGhAQdLJZNaKpL0t5JX8V8vR7P2YqH4nM6K0"
}

# Credit Card Storage (INSECURE - Should never store credit cards)
CUSTOMER_CREDIT_CARDS = {
    "customer_123": {
        "card_number": "4532-1234-5678-9010",
        "expiry": "12/25",
        "cvv": "123",
        "name": "John Doe"
    }
}
