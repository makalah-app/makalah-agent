"""
Agent-Makalah Backend Configuration
Environment variables and application settings management
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    
    # === API Configuration ===
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    log_level: str = "info"
    
    # === AI/LLM Provider Keys ===
    openai_api_key: Optional[str] = None
    google_gemini_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # === Supabase Configuration ===
    supabase_url: Optional[str] = None
    supabase_anon_key: Optional[str] = None
    supabase_service_role_key: Optional[str] = None
    supabase_project_ref: Optional[str] = None
    supabase_project_id: Optional[str] = None
    supabase_jwt_secret: Optional[str] = None
    supabase_storage_url: Optional[str] = None
    s3_endpoint: Optional[str] = None
    
    # === Database Configuration ===
    database_url: Optional[str] = None
    postgres_db: str = "postgres"
    postgres_user: str = "postgres"
    postgres_password: Optional[str] = None
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    
    # === Redis Configuration ===
    redis_url: str = "redis://localhost:6379/0"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    
    # === Upstash Redis Configuration ===
    upstash_redis_url: Optional[str] = None
    upstash_redis_token: Optional[str] = None
    upstash_redis_password: Optional[str] = None
    upstash_redis_endpoint: Optional[str] = None
    upstash_redis_port: Optional[int] = None
    
    # === JWT Authentication Configuration ===
    jwt_secret_key: str = "default-jwt-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7
    
    # === Password Hashing Configuration ===
    password_hash_algorithm: str = "bcrypt"
    password_hash_rounds: int = 12
    password_salt: str = "default-salt-change-in-production"
    
    # === Session Configuration ===
    session_secret_key: str = "default-session-secret-change-in-production"
    session_max_age: int = 3600  # 1 hour
    session_cookie_name: str = "agent_makalah_session"
    session_cookie_secure: bool = False  # Set to True in production with HTTPS
    session_cookie_httponly: bool = True
    session_cookie_samesite: str = "lax"
    
    # === Google Cloud Configuration ===
    gcs_bucket_name: Optional[str] = None
    google_cloud_project: Optional[str] = None
    google_application_credentials: Optional[str] = None
    
    # === External APIs ===
    serper_api_key: Optional[str] = None
    google_search_api_key: Optional[str] = None
    google_search_engine_id: Optional[str] = None
    
    # === Security Configuration ===
    secret_key: str = "default-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    
    # === Application Settings ===
    environment: str = "development"
    debug: bool = True
    allowed_hosts: List[str] = ["localhost", "127.0.0.1"]
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # === File Upload Configuration ===
    max_file_size_mb: int = 50
    allowed_file_types: List[str] = ["pdf", "docx", "txt"]
    upload_dir: str = "uploads"
    
    # === Agent System Configuration ===
    max_concurrent_agents: int = 6
    agent_timeout_seconds: int = 300
    session_timeout_minutes: int = 60
    
    # === Academic Writing Configuration ===
    default_language: str = "id"  # Indonesian
    max_paper_length_words: int = 10000
    max_revision_cycles: int = 3
    
    class Config:
        # Construct the path to the .env file relative to this config.py file
        # Assuming config.py is in src/core/ and .env is in the project root (two levels up)
        # BASE_DIR should point to the project root
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"
        case_sensitive = False

# Global settings instance
settings = Settings()

def get_database_url() -> str:
    """
    Construct database URL from individual components
    """
    if settings.database_url:
        return settings.database_url
    
    return (
        f"postgresql://{settings.postgres_user}:{settings.postgres_password}"
        f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
    )

def get_redis_url() -> str:
    """
    Get Redis connection URL
    """
    return settings.redis_url

def get_upstash_redis_url() -> str:
    """
    Get Upstash Redis connection URL
    """
    if settings.upstash_redis_url:
        return settings.upstash_redis_url
    return None

def is_development() -> bool:
    """
    Check if running in development mode
    """
    return settings.environment.lower() == "development"

def is_production() -> bool:
    """
    Check if running in production mode
    """
    return settings.environment.lower() == "production" 