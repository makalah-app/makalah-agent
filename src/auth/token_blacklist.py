"""
JWT Token Blacklist Manager - Agent Makalah Backend
Handles token revocation and blacklisting using Redis for distributed blacklist storage
"""

import json
from datetime import datetime, timedelta
from typing import Optional, List, Set
from upstash_redis import Redis
from src.core.config import settings
from src.auth.jwt_utils import decode_token, get_token_expiry


class TokenBlacklist:
    """
    Manages JWT token blacklisting and revocation using Redis
    """
    
    def __init__(self):
        """Initialize token blacklist with Upstash Redis connection"""
        self.redis = None
        if settings.upstash_redis_url and settings.upstash_redis_token:
            try:
                self.redis = Redis(
                    url=settings.upstash_redis_url,
                    token=settings.upstash_redis_token
                )
            except Exception as e:
                print(f"Failed to connect to Upstash Redis for blacklist: {e}")
                self.redis = None
    
    def _get_blacklist_key(self, token_jti: str) -> str:
        """Generate Redis key for blacklisted token"""
        return f"blacklist:agent_makalah:{token_jti}"
    
    def _get_user_tokens_key(self, user_id: str) -> str:
        """Generate Redis key for user's active tokens"""
        return f"user_tokens:agent_makalah:{user_id}"
    
    def _extract_jti(self, token: str) -> Optional[str]:
        """
        Extract JTI (JWT ID) from token
        
        Args:
            token: JWT token string
            
        Returns:
            Optional[str]: JTI if found, None otherwise
        """
        payload = decode_token(token)
        if payload:
            # If JTI not present, use a combination of sub and iat as unique identifier
            if 'jti' in payload:
                return payload['jti']
            elif 'sub' in payload and 'iat' in payload:
                return f"{payload['sub']}:{payload['iat']}"
        return None
    
    def blacklist_token(self, token: str, reason: str = "user_logout") -> bool:
        """
        Add token to blacklist
        
        Args:
            token: JWT token to blacklist
            reason: Reason for blacklisting (logout, revoked, etc.)
            
        Returns:
            bool: True if token blacklisted successfully, False otherwise
        """
        if not self.redis:
            print("Redis not available for token blacklisting")
            return False
        
        jti = self._extract_jti(token)
        if not jti:
            print("Could not extract JTI from token")
            return False
        
        try:
            # Get token expiry to set TTL
            expiry = get_token_expiry(token)
            if not expiry:
                print("Could not determine token expiry")
                return False
            
            # Calculate TTL (time until token expires)
            ttl_seconds = int((expiry - datetime.utcnow()).total_seconds())
            if ttl_seconds <= 0:
                # Token already expired, no need to blacklist
                return True
            
            # Blacklist entry data
            blacklist_data = {
                "blacklisted_at": datetime.utcnow().isoformat(),
                "reason": reason,
                "expires_at": expiry.isoformat()
            }
            
            key = self._get_blacklist_key(jti)
            result = self.redis.setex(
                key,
                ttl_seconds,
                json.dumps(blacklist_data)
            )
            
            print(f"Token {jti} blacklisted until {expiry}, reason: {reason}")
            return result
            
        except Exception as e:
            print(f"Failed to blacklist token: {e}")
            return False
    
    def is_token_blacklisted(self, token: str) -> bool:
        """
        Check if token is blacklisted
        
        Args:
            token: JWT token to check
            
        Returns:
            bool: True if token is blacklisted, False otherwise
        """
        if not self.redis:
            return False
        
        jti = self._extract_jti(token)
        if not jti:
            return False
        
        try:
            key = self._get_blacklist_key(jti)
            result = self.redis.get(key)
            return result is not None
            
        except Exception as e:
            print(f"Failed to check token blacklist status: {e}")
            return False
    
    def blacklist_all_user_tokens(self, user_id: str, reason: str = "security_revocation") -> int:
        """
        Blacklist all active tokens for a user
        
        Args:
            user_id: User identifier
            reason: Reason for mass revocation
            
        Returns:
            int: Number of tokens blacklisted
        """
        if not self.redis:
            return 0
        
        try:
            # Get all active tokens for user
            user_tokens_key = self._get_user_tokens_key(user_id)
            active_tokens = self.redis.smembers(user_tokens_key)
            
            blacklisted_count = 0
            
            for token_jti in active_tokens:
                try:
                    # Blacklist each token
                    blacklist_data = {
                        "blacklisted_at": datetime.utcnow().isoformat(),
                        "reason": reason,
                        "user_revocation": True
                    }
                    
                    blacklist_key = self._get_blacklist_key(token_jti)
                    # Set a reasonable TTL (24 hours) for mass revocation
                    self.redis.setex(
                        blacklist_key,
                        86400,  # 24 hours
                        json.dumps(blacklist_data)
                    )
                    blacklisted_count += 1
                    
                except Exception as e:
                    print(f"Failed to blacklist token {token_jti}: {e}")
            
            # Clear the user's active tokens set
            self.redis.delete(user_tokens_key)
            
            print(f"Blacklisted {blacklisted_count} tokens for user {user_id}")
            return blacklisted_count
            
        except Exception as e:
            print(f"Failed to blacklist user tokens: {e}")
            return 0
    
    def track_user_token(self, user_id: str, token: str) -> bool:
        """
        Track a token as active for a user
        
        Args:
            user_id: User identifier
            token: JWT token to track
            
        Returns:
            bool: True if tracking successful, False otherwise
        """
        if not self.redis:
            return False
        
        jti = self._extract_jti(token)
        if not jti:
            return False
        
        try:
            user_tokens_key = self._get_user_tokens_key(user_id)
            
            # Add token to user's active tokens set
            self.redis.sadd(user_tokens_key, jti)
            
            # Set expiry for the user tokens set
            expiry = get_token_expiry(token)
            if expiry:
                ttl_seconds = int((expiry - datetime.utcnow()).total_seconds())
                if ttl_seconds > 0:
                    self.redis.expire(user_tokens_key, ttl_seconds)
            
            return True
            
        except Exception as e:
            print(f"Failed to track user token: {e}")
            return False
    
    def untrack_user_token(self, user_id: str, token: str) -> bool:
        """
        Remove token from user's active tokens
        
        Args:
            user_id: User identifier
            token: JWT token to untrack
            
        Returns:
            bool: True if untracking successful, False otherwise
        """
        if not self.redis:
            return False
        
        jti = self._extract_jti(token)
        if not jti:
            return False
        
        try:
            user_tokens_key = self._get_user_tokens_key(user_id)
            result = self.redis.srem(user_tokens_key, jti)
            return result == 1
            
        except Exception as e:
            print(f"Failed to untrack user token: {e}")
            return False
    
    def get_blacklist_stats(self) -> dict:
        """
        Get blacklist statistics
        
        Returns:
            dict: Statistics about blacklisted tokens
        """
        if not self.redis:
            return {"error": "Redis not available"}
        
        try:
            # Use Redis SCAN to count blacklisted tokens
            pattern = "blacklist:agent_makalah:*"
            cursor = 0
            blacklisted_count = 0
            
            while True:
                cursor, keys = self.redis.scan(cursor, match=pattern, count=100)
                blacklisted_count += len(keys)
                if cursor == 0:
                    break
            
            return {
                "total_blacklisted": blacklisted_count,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Failed to get statistics: {e}"}
    
    def cleanup_expired_blacklist(self) -> int:
        """
        Clean up expired blacklist entries (Redis handles this automatically with TTL)
        This method is for monitoring purposes
        
        Returns:
            int: Number of entries cleaned up (always 0 as Redis handles TTL)
        """
        # Redis automatically handles TTL expiration
        # This method exists for compatibility and monitoring
        return 0


# Global token blacklist instance
token_blacklist = TokenBlacklist() 