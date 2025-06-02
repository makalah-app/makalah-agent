"""
Authentication module for Agent-Makalah Backend
Comprehensive authentication system with JWT tokens, session management, and security features
"""

# JWT Token Management
from .jwt_utils import (
    create_access_token,
    create_refresh_token, 
    create_token_pair,
    verify_token,
    verify_refresh_token,
    decode_token,
    get_token_expiry,
    is_token_expired,
    get_token_jti,
    get_user_id_from_token,
    refresh_access_token,
    validate_and_decode_token,
    get_token_remaining_time,
    is_token_near_expiry
)

# Password Management
from .password_utils import hash_password, verify_password

# Session Management  
from .session_manager import SessionManager, session_manager

# Enhanced Session Management with JWT Integration
from .enhanced_session_manager import EnhancedSessionManager, enhanced_session_manager

# Token Blacklisting
from .token_blacklist import TokenBlacklist, token_blacklist

__all__ = [
    # JWT Token Management
    "create_access_token",
    "create_refresh_token",
    "create_token_pair", 
    "verify_token",
    "verify_refresh_token",
    "decode_token",
    "get_token_expiry",
    "is_token_expired",
    "get_token_jti",
    "get_user_id_from_token",
    "refresh_access_token",
    "validate_and_decode_token",
    "get_token_remaining_time",
    "is_token_near_expiry",
    
    # Password Management
    "hash_password",
    "verify_password",
    
    # Session Management
    "SessionManager", 
    "session_manager",
    
    # Enhanced Session Management  
    "EnhancedSessionManager",
    "enhanced_session_manager",
    
    # Token Blacklisting
    "TokenBlacklist",
    "token_blacklist"
] 