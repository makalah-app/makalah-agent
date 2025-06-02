"""
JWT Token Management Utilities
Handles creation, verification, and decoding of JWT tokens for Agent-Makalah authentication
"""

import uuid
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from jose import JWTError, jwt
from src.core.config import settings


def create_access_token(
    data: Dict[str, Any], 
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token with user data and expiration
    
    Args:
        data: Dictionary containing user data to encode in token
        expires_delta: Optional custom expiration time
        
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    
    # Generate unique JTI (JWT ID) for token tracking
    jti = str(uuid.uuid4())
    
    if expires_delta:
        expire_seconds = int(expires_delta.total_seconds())
    else:
        expire_seconds = settings.jwt_access_token_expire_minutes * 60
    
    current_time = int(time.time())
    
    to_encode.update({
        "exp": current_time + expire_seconds, 
        "iat": current_time,
        "jti": jti,
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.jwt_secret_key, 
        algorithm=settings.jwt_algorithm
    )
    
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Create a JWT refresh token with longer expiration
    
    Args:
        data: Dictionary containing user data to encode in token
        
    Returns:
        str: Encoded JWT refresh token
    """
    to_encode = data.copy()
    
    # Generate unique JTI for refresh token
    jti = str(uuid.uuid4())
    expire_seconds = settings.jwt_refresh_token_expire_days * 24 * 60 * 60  # days to seconds
    
    current_time = int(time.time())
    
    to_encode.update({
        "exp": current_time + expire_seconds, 
        "iat": current_time,
        "jti": jti,
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.jwt_secret_key, 
        algorithm=settings.jwt_algorithm
    )
    
    return encoded_jwt


def create_token_pair(user_data: Dict[str, Any]) -> Tuple[str, str]:
    """
    Create access and refresh token pair for a user
    
    Args:
        user_data: Dictionary containing user data to encode in tokens
        
    Returns:
        Tuple[str, str]: (access_token, refresh_token)
    """
    access_token = create_access_token(user_data)
    refresh_token = create_refresh_token(user_data)
    
    return access_token, refresh_token


def verify_token(token: str, token_type: Optional[str] = None) -> bool:
    """
    Verify if a JWT token is valid
    
    Args:
        token: JWT token to verify
        token_type: Expected token type ('access' or 'refresh')
        
    Returns:
        bool: True if token is valid, False otherwise
    """
    # Handle None and empty token cases
    if not token or token is None:
        return False
        
    try:
        payload = jwt.decode(
            token, 
            settings.jwt_secret_key, 
            algorithms=[settings.jwt_algorithm]
        )
        
        # Check token type if specified
        if token_type and payload.get("type") != token_type:
            return False
            
        return True
    except JWTError:
        return False


def verify_refresh_token(token: str) -> bool:
    """
    Verify if a refresh token is valid
    
    Args:
        token: Refresh token to verify
        
    Returns:
        bool: True if refresh token is valid, False otherwise
    """
    return verify_token(token, token_type="refresh")


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode a JWT token and return the payload
    
    Args:
        token: JWT token to decode
        
    Returns:
        Optional[Dict[str, Any]]: Token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token, 
            settings.jwt_secret_key, 
            algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError:
        return None


def get_token_expiry(token: str) -> Optional[datetime]:
    """
    Get expiration time from a JWT token
    
    Args:
        token: JWT token to check
        
    Returns:
        Optional[datetime]: Token expiration time if valid, None otherwise
    """
    payload = decode_token(token)
    if payload and "exp" in payload:
        return datetime.fromtimestamp(payload["exp"])
    return None


def is_token_expired(token: str) -> bool:
    """
    Check if a JWT token is expired
    
    Args:
        token: JWT token to check
        
    Returns:
        bool: True if token is expired, False otherwise
    """
    payload = decode_token(token)
    if payload and "exp" in payload:
        exp_timestamp = payload["exp"]
        current_timestamp = int(time.time())
        return current_timestamp >= exp_timestamp
    return True  # Consider invalid tokens as expired


def get_token_jti(token: str) -> Optional[str]:
    """
    Extract JTI (JWT ID) from token
    
    Args:
        token: JWT token to extract JTI from
        
    Returns:
        Optional[str]: JTI if found, None otherwise
    """
    payload = decode_token(token)
    if payload:
        return payload.get("jti")
    return None


def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user ID from token
    
    Args:
        token: JWT token to extract user ID from
        
    Returns:
        Optional[str]: User ID if found, None otherwise
    """
    payload = decode_token(token)
    if payload:
        return payload.get("sub")
    return None


def refresh_access_token(refresh_token: str) -> Optional[str]:
    """
    Generate new access token from valid refresh token
    
    Args:
        refresh_token: Valid refresh token
        
    Returns:
        Optional[str]: New access token if refresh token is valid, None otherwise
    """
    # Verify refresh token
    if not verify_refresh_token(refresh_token):
        return None
    
    # Check if token is blacklisted (import here to avoid circular import)
    try:
        from src.auth.token_blacklist import token_blacklist
        if token_blacklist.is_token_blacklisted(refresh_token):
            return None
    except ImportError:
        pass  # Blacklist not available
    
    # Decode refresh token to get user data
    payload = decode_token(refresh_token)
    if not payload:
        return None
    
    # Create new access token with same user data
    user_data = {
        "sub": payload.get("sub"),
        "email": payload.get("email"),
        "is_superuser": payload.get("is_superuser", False)
    }
    
    return create_access_token(user_data)


def validate_and_decode_token(token: str, check_blacklist: bool = True) -> Optional[Dict[str, Any]]:
    """
    Comprehensive token validation including blacklist check
    
    Args:
        token: JWT token to validate
        check_blacklist: Whether to check token blacklist
        
    Returns:
        Optional[Dict[str, Any]]: Token payload if valid, None otherwise
    """
    # First verify token structure and signature
    if not verify_token(token):
        return None
    
    # Check if token is blacklisted
    if check_blacklist:
        try:
            from src.auth.token_blacklist import token_blacklist
            if token_blacklist.is_token_blacklisted(token):
                return None
        except ImportError:
            pass  # Blacklist not available
    
    # Decode and return payload
    return decode_token(token)


def get_token_remaining_time(token: str) -> Optional[timedelta]:
    """
    Get remaining time until token expires
    
    Args:
        token: JWT token to check
        
    Returns:
        Optional[timedelta]: Remaining time if token valid, None otherwise
    """
    payload = decode_token(token)
    if payload and "exp" in payload:
        exp_timestamp = payload["exp"]
        current_timestamp = int(time.time())
        remaining_seconds = exp_timestamp - current_timestamp
        return timedelta(seconds=remaining_seconds) if remaining_seconds > 0 else timedelta(0)
    return None


def is_token_near_expiry(token: str, threshold_minutes: int = 15) -> bool:
    """
    Check if token is near expiry (within threshold)
    
    Args:
        token: JWT token to check
        threshold_minutes: Minutes before expiry to consider "near"
        
    Returns:
        bool: True if token expires within threshold, False otherwise
    """
    remaining = get_token_remaining_time(token)
    if remaining:
        threshold = timedelta(minutes=threshold_minutes)
        return remaining <= threshold
    return True  # Consider invalid tokens as expired 