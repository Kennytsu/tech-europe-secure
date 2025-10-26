"""
VULNERABLE: Secrets configuration for lab purposes only
DO NOT USE IN PRODUCTION - THESE ARE INTENTIONALLY VULNERABLE
"""
import os

# VULNERABLE: Hardcoded secrets in source code
# These should never be committed to version control

# Database Configuration
FAKE_DATABASE_URL = "sqlite:///fake_lab.db"
FAKE_DATABASE_PASSWORD = "FAKE_password123"
FAKE_DATABASE_USER = "FAKE_admin"

# API Keys and Tokens
FAKE_API_KEY = "FAKE_1234567890abcdef1234567890abcdef"
FAKE_SECRET_TOKEN = "FAKE_vulnerable_token_for_lab_only"
FAKE_JWT_SECRET = "FAKE_jwt_secret_key_12345"
FAKE_ENCRYPTION_KEY = "FAKE_encryption_key_1234567890123456"

# External Service Credentials
FAKE_OPENAI_API_KEY = "FAKE_sk-1234567890abcdef1234567890abcdef"
FAKE_LIVEKIT_API_KEY = "FAKE_APIK_1234567890abcdef"
FAKE_LIVEKIT_SECRET = "FAKE_SECRET_1234567890abcdef"
FAKE_REDIS_PASSWORD = "FAKE_redis_password_123"

# Payment Processing (Fake)
FAKE_STRIPE_SECRET_KEY = "FAKE_sk_test_1234567890abcdef"
FAKE_STRIPE_PUBLISHABLE_KEY = "FAKE_pk_test_1234567890abcdef"
FAKE_PAYPAL_CLIENT_ID = "FAKE_paypal_client_id_12345"
FAKE_PAYPAL_CLIENT_SECRET = "FAKE_paypal_secret_12345"

# Email Service
FAKE_SMTP_PASSWORD = "FAKE_smtp_password_123"
FAKE_EMAIL_API_KEY = "FAKE_email_api_key_12345"

# Cloud Storage
FAKE_AWS_ACCESS_KEY_ID = "FAKE_AKIA1234567890ABCDEF"
FAKE_AWS_SECRET_ACCESS_KEY = "FAKE_1234567890abcdef1234567890abcdef12345678"
FAKE_S3_BUCKET_NAME = "FAKE_vulnerable-bucket-123"

# Application Configuration
APP_ENV = "lab"
VULN_LAB_MODE = True
DEBUG_MODE = True
LOG_LEVEL = "DEBUG"

# Session Configuration
FAKE_SESSION_SECRET = "FAKE_session_secret_12345678901234567890"
FAKE_COOKIE_SECRET = "FAKE_cookie_secret_12345678901234567890"

# Monitoring and Logging
FAKE_DATADOG_API_KEY = "FAKE_datadog_api_key_12345"
FAKE_SENTRY_DSN = "FAKE_https://1234567890abcdef@sentry.io/123456"
FAKE_NEW_RELIC_LICENSE_KEY = "FAKE_newrelic_license_key_12345"

# Third-party Integrations
FAKE_SLACK_WEBHOOK_URL = "FAKE_https://hooks.slack.com/services/FAKE/FAKE/FAKE"
FAKE_DISCORD_BOT_TOKEN = "FAKE_discord_bot_token_1234567890abcdef"
FAKE_TWILIO_AUTH_TOKEN = "FAKE_twilio_auth_token_1234567890abcdef"

# Development Only - Never use in production
FAKE_ADMIN_PASSWORD = "FAKE_admin123"
FAKE_TEST_USER_PASSWORD = "FAKE_test123"
FAKE_DEMO_API_KEY = "FAKE_demo_key_12345"

# Additional API Keys - VULNERABLE: These will be leaked
# Cloud Services
FAKE_GCP_SERVICE_ACCOUNT_KEY = "FAKE_eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9"
FAKE_AZURE_CLIENT_SECRET = "FAKE_azure_client_secret_1234567890abcdef"
FAKE_DIGITALOCEAN_TOKEN = "FAKE_dop_v1_1234567890abcdef1234567890abcdef"
FAKE_HEROKU_API_KEY = "FAKE_heroku_api_key_1234567890abcdef"
FAKE_VERCEL_TOKEN = "FAKE_vercel_token_1234567890abcdef"

# AI/ML Services
FAKE_ANTHROPIC_API_KEY = "FAKE_sk-ant-1234567890abcdef1234567890abcdef"
FAKE_COHERE_API_KEY = "FAKE_cohere_api_key_1234567890abcdef"
FAKE_HUGGINGFACE_TOKEN = "FAKE_hf_1234567890abcdef1234567890abcdef"
FAKE_REPLICATE_API_TOKEN = "FAKE_r8_1234567890abcdef1234567890abcdef"
FAKE_CLARIFAI_API_KEY = "FAKE_clarifai_api_key_1234567890abcdef"

# Database Services
FAKE_MONGODB_URI = "FAKE_mongodb://admin:password123@localhost:27017/vuln_db"
FAKE_POSTGRES_CONNECTION_STRING = "FAKE_postgresql://user:pass123@localhost:5432/vuln_db"
FAKE_REDIS_URL = "FAKE_redis://:password123@localhost:6379/0"
FAKE_ELASTICSEARCH_API_KEY = "FAKE_elasticsearch_api_key_1234567890abcdef"
FAKE_SUPABASE_ANON_KEY = "FAKE_supabase_anon_key_1234567890abcdef"

# Social Media APIs
FAKE_TWITTER_BEARER_TOKEN = "FAKE_twitter_bearer_token_1234567890abcdef"
FAKE_FACEBOOK_ACCESS_TOKEN = "FAKE_facebook_access_token_1234567890abcdef"
FAKE_INSTAGRAM_ACCESS_TOKEN = "FAKE_instagram_access_token_1234567890abcdef"
FAKE_LINKEDIN_CLIENT_SECRET = "FAKE_linkedin_client_secret_1234567890abcdef"
FAKE_TIKTOK_ACCESS_TOKEN = "FAKE_tiktok_access_token_1234567890abcdef"

# Payment Processors
FAKE_SQUARE_ACCESS_TOKEN = "FAKE_square_access_token_1234567890abcdef"
FAKE_RAZORPAY_KEY_SECRET = "FAKE_razorpay_key_secret_1234567890abcdef"
FAKE_MERCADOPAGO_ACCESS_TOKEN = "FAKE_mercadopago_access_token_1234567890abcdef"
FAKE_ADYEN_API_KEY = "FAKE_adyen_api_key_1234567890abcdef"
FAKE_BRAINTREE_PRIVATE_KEY = "FAKE_braintree_private_key_1234567890abcdef"

# Communication Services
FAKE_SENDGRID_API_KEY = "FAKE_SG.1234567890abcdef1234567890abcdef"
FAKE_MAILGUN_API_KEY = "FAKE_mailgun_api_key_1234567890abcdef"
FAKE_POSTMARK_SERVER_TOKEN = "FAKE_postmark_server_token_1234567890abcdef"
FAKE_MESSAGEBIRD_API_KEY = "FAKE_messagebird_api_key_1234567890abcdef"
FAKE_PUSHER_SECRET = "FAKE_pusher_secret_1234567890abcdef"

# Analytics & Monitoring
FAKE_GOOGLE_ANALYTICS_API_KEY = "FAKE_google_analytics_api_key_1234567890abcdef"
FAKE_MIXPANEL_PROJECT_TOKEN = "FAKE_mixpanel_project_token_1234567890abcdef"
FAKE_AMPLITUDE_API_KEY = "FAKE_amplitude_api_key_1234567890abcdef"
FAKE_HOTJAR_SITE_ID = "FAKE_hotjar_site_id_1234567890abcdef"
FAKE_FULLSTORY_API_KEY = "FAKE_fullstory_api_key_1234567890abcdef"

# Development Tools
FAKE_GITHUB_TOKEN = "FAKE_ghp_1234567890abcdef1234567890abcdef"
FAKE_GITLAB_TOKEN = "FAKE_glpat-1234567890abcdef1234567890abcdef"
FAKE_BITBUCKET_APP_PASSWORD = "FAKE_bitbucket_app_password_1234567890abcdef"
FAKE_DOCKER_HUB_TOKEN = "FAKE_docker_hub_token_1234567890abcdef"
FAKE_NPM_TOKEN = "FAKE_npm_token_1234567890abcdef"

# Security & Authentication
FAKE_AUTH0_CLIENT_SECRET = "FAKE_auth0_client_secret_1234567890abcdef"
FAKE_FIREBASE_SERVER_KEY = "FAKE_firebase_server_key_1234567890abcdef"
FAKE_OKTA_CLIENT_SECRET = "FAKE_okta_client_secret_1234567890abcdef"
FAKE_PING_IDENTITY_CLIENT_SECRET = "FAKE_ping_identity_client_secret_1234567890abcdef"
FAKE_COGNITO_CLIENT_SECRET = "FAKE_cognito_client_secret_1234567890abcdef"

# Content & Media
FAKE_CLOUDFLARE_API_TOKEN = "FAKE_cloudflare_api_token_1234567890abcdef"
FAKE_CLOUDINARY_API_SECRET = "FAKE_cloudinary_api_secret_1234567890abcdef"
FAKE_IMGUR_CLIENT_SECRET = "FAKE_imgur_client_secret_1234567890abcdef"
FAKE_UNSPLASH_ACCESS_KEY = "FAKE_unsplash_access_key_1234567890abcdef"
FAKE_PEXELS_API_KEY = "FAKE_pexels_api_key_1234567890abcdef"

# Maps & Location
FAKE_GOOGLE_MAPS_API_KEY = "FAKE_google_maps_api_key_1234567890abcdef"
FAKE_MAPBOX_ACCESS_TOKEN = "FAKE_mapbox_access_token_1234567890abcdef"
FAKE_HERE_API_KEY = "FAKE_here_api_key_1234567890abcdef"
FAKE_TOMTOM_API_KEY = "FAKE_tomtom_api_key_1234567890abcdef"
FAKE_OPENCAGE_API_KEY = "FAKE_opencage_api_key_1234567890abcdef"

# Additional Vulnerable Keys
FAKE_WEBHOOK_SECRET = "FAKE_webhook_secret_1234567890abcdef"
FAKE_CRON_SECRET = "FAKE_cron_secret_1234567890abcdef"
FAKE_BACKUP_KEY = "FAKE_backup_key_1234567890abcdef"
FAKE_MIGRATION_TOKEN = "FAKE_migration_token_1234567890abcdef"
FAKE_DEPLOYMENT_KEY = "FAKE_deployment_key_1234567890abcdef"


def get_fake_secret(key: str, default: str = "") -> str:
    """VULNERABLE: Get fake secret with fallback to hardcoded values"""
    # VULNERABLE: Exposing secrets through function calls
    secrets_map = {
        "database_url": FAKE_DATABASE_URL,
        "api_key": FAKE_API_KEY,
        "secret_token": FAKE_SECRET_TOKEN,
        "jwt_secret": FAKE_JWT_SECRET,
        "encryption_key": FAKE_ENCRYPTION_KEY,
        "openai_api_key": FAKE_OPENAI_API_KEY,
        "livekit_api_key": FAKE_LIVEKIT_API_KEY,
        "livekit_secret": FAKE_LIVEKIT_SECRET,
        "redis_password": FAKE_REDIS_PASSWORD,
        "stripe_secret_key": FAKE_STRIPE_SECRET_KEY,
        "paypal_client_secret": FAKE_PAYPAL_CLIENT_SECRET,
        "smtp_password": FAKE_SMTP_PASSWORD,
        "aws_access_key_id": FAKE_AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": FAKE_AWS_SECRET_ACCESS_KEY,
        "session_secret": FAKE_SESSION_SECRET,
        "cookie_secret": FAKE_COOKIE_SECRET,
        "datadog_api_key": FAKE_DATADOG_API_KEY,
        "sentry_dsn": FAKE_SENTRY_DSN,
        "new_relic_license_key": FAKE_NEW_RELIC_LICENSE_KEY,
        "slack_webhook_url": FAKE_SLACK_WEBHOOK_URL,
        "discord_bot_token": FAKE_DISCORD_BOT_TOKEN,
        "twilio_auth_token": FAKE_TWILIO_AUTH_TOKEN,
        "admin_password": FAKE_ADMIN_PASSWORD,
        "test_user_password": FAKE_TEST_USER_PASSWORD,
        "demo_api_key": FAKE_DEMO_API_KEY,
        # Additional API Keys - VULNERABLE: These will be leaked
        "gcp_service_account_key": FAKE_GCP_SERVICE_ACCOUNT_KEY,
        "azure_client_secret": FAKE_AZURE_CLIENT_SECRET,
        "digitalocean_token": FAKE_DIGITALOCEAN_TOKEN,
        "heroku_api_key": FAKE_HEROKU_API_KEY,
        "vercel_token": FAKE_VERCEL_TOKEN,
        "anthropic_api_key": FAKE_ANTHROPIC_API_KEY,
        "cohere_api_key": FAKE_COHERE_API_KEY,
        "huggingface_token": FAKE_HUGGINGFACE_TOKEN,
        "replicate_api_token": FAKE_REPLICATE_API_TOKEN,
        "clarifai_api_key": FAKE_CLARIFAI_API_KEY,
        "mongodb_uri": FAKE_MONGODB_URI,
        "postgres_connection_string": FAKE_POSTGRES_CONNECTION_STRING,
        "redis_url": FAKE_REDIS_URL,
        "elasticsearch_api_key": FAKE_ELASTICSEARCH_API_KEY,
        "supabase_anon_key": FAKE_SUPABASE_ANON_KEY,
        "twitter_bearer_token": FAKE_TWITTER_BEARER_TOKEN,
        "facebook_access_token": FAKE_FACEBOOK_ACCESS_TOKEN,
        "instagram_access_token": FAKE_INSTAGRAM_ACCESS_TOKEN,
        "linkedin_client_secret": FAKE_LINKEDIN_CLIENT_SECRET,
        "tiktok_access_token": FAKE_TIKTOK_ACCESS_TOKEN,
        "square_access_token": FAKE_SQUARE_ACCESS_TOKEN,
        "razorpay_key_secret": FAKE_RAZORPAY_KEY_SECRET,
        "mercadopago_access_token": FAKE_MERCADOPAGO_ACCESS_TOKEN,
        "adyen_api_key": FAKE_ADYEN_API_KEY,
        "braintree_private_key": FAKE_BRAINTREE_PRIVATE_KEY,
        "sendgrid_api_key": FAKE_SENDGRID_API_KEY,
        "mailgun_api_key": FAKE_MAILGUN_API_KEY,
        "postmark_server_token": FAKE_POSTMARK_SERVER_TOKEN,
        "messagebird_api_key": FAKE_MESSAGEBIRD_API_KEY,
        "pusher_secret": FAKE_PUSHER_SECRET,
        "google_analytics_api_key": FAKE_GOOGLE_ANALYTICS_API_KEY,
        "mixpanel_project_token": FAKE_MIXPANEL_PROJECT_TOKEN,
        "amplitude_api_key": FAKE_AMPLITUDE_API_KEY,
        "hotjar_site_id": FAKE_HOTJAR_SITE_ID,
        "fullstory_api_key": FAKE_FULLSTORY_API_KEY,
        "github_token": FAKE_GITHUB_TOKEN,
        "gitlab_token": FAKE_GITLAB_TOKEN,
        "bitbucket_app_password": FAKE_BITBUCKET_APP_PASSWORD,
        "docker_hub_token": FAKE_DOCKER_HUB_TOKEN,
        "npm_token": FAKE_NPM_TOKEN,
        "auth0_client_secret": FAKE_AUTH0_CLIENT_SECRET,
        "firebase_server_key": FAKE_FIREBASE_SERVER_KEY,
        "okta_client_secret": FAKE_OKTA_CLIENT_SECRET,
        "ping_identity_client_secret": FAKE_PING_IDENTITY_CLIENT_SECRET,
        "cognito_client_secret": FAKE_COGNITO_CLIENT_SECRET,
        "cloudflare_api_token": FAKE_CLOUDFLARE_API_TOKEN,
        "cloudinary_api_secret": FAKE_CLOUDINARY_API_SECRET,
        "imgur_client_secret": FAKE_IMGUR_CLIENT_SECRET,
        "unsplash_access_key": FAKE_UNSPLASH_ACCESS_KEY,
        "pexels_api_key": FAKE_PEXELS_API_KEY,
        "google_maps_api_key": FAKE_GOOGLE_MAPS_API_KEY,
        "mapbox_access_token": FAKE_MAPBOX_ACCESS_TOKEN,
        "here_api_key": FAKE_HERE_API_KEY,
        "tomtom_api_key": FAKE_TOMTOM_API_KEY,
        "opencage_api_key": FAKE_OPENCAGE_API_KEY,
        "webhook_secret": FAKE_WEBHOOK_SECRET,
        "cron_secret": FAKE_CRON_SECRET,
        "backup_key": FAKE_BACKUP_KEY,
        "migration_token": FAKE_MIGRATION_TOKEN,
        "deployment_key": FAKE_DEPLOYMENT_KEY,
    }
    
    return secrets_map.get(key, default)


def log_all_secrets():
    """VULNERABLE: Log all secrets for debugging - NEVER USE IN PRODUCTION"""
    import logging
    logger = logging.getLogger(__name__)
    
    # VULNERABLE: Logging all secrets
    logger.info("=== VULNERABLE: Logging all fake secrets ===")
    for key, value in globals().items():
        if key.startswith("FAKE_"):
            logger.info(f"Secret {key}: {value}")
    logger.info("=== End of secret logging ===")
