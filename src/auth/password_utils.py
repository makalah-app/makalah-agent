"""
Password Hashing Utilities
Secure password hashing and verification using bcrypt for Agent-Makalah authentication
"""

from passlib.context import CryptContext
from src.core.config import settings

# Create password context for bcrypt hashing
pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto",
    bcrypt__rounds=settings.password_hash_rounds
)


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt
    
    Args:
        password: Plain text password to hash
        
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against its hash
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Stored hash to verify against
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def is_password_strong(password: str) -> tuple[bool, list[str]]:
    """
    Check if password meets Agent-Makalah security requirements
    
    Args:
        password: Password to validate
        
    Returns:
        tuple[bool, list[str]]: (is_valid, list_of_requirements_not_met)
    """
    requirements = []
    
    if len(password) < 8:
        requirements.append("Password must be at least 8 characters long")
    
    if not any(char.isupper() for char in password):
        requirements.append("Password must contain at least one uppercase letter")
    
    if not any(char.islower() for char in password):
        requirements.append("Password must contain at least one lowercase letter")
    
    if not any(char.isdigit() for char in password):
        requirements.append("Password must contain at least one number")
    
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(char in special_chars for char in password):
        requirements.append("Password must contain at least one special character")
    
    return len(requirements) == 0, requirements


def generate_password_reset_token() -> str:
    """
    Generate a secure token for password reset
    
    Returns:
        str: Random secure token for password reset
    """
    import secrets
    return secrets.token_urlsafe(32) 