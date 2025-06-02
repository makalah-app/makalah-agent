"""
Session Management for Agent-Makalah
Handles user sessions using Upstash Redis for distributed session storage
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from upstash_redis import Redis
from src.core.config import settings


class SessionManager:
    """
    Manages user sessions with Redis storage
    """
    
    def __init__(self):
        """Initialize session manager with Upstash Redis connection"""
        self.redis = None
        if settings.upstash_redis_url and settings.upstash_redis_token:
            try:
                self.redis = Redis(
                    url=settings.upstash_redis_url,
                    token=settings.upstash_redis_token
                )
            except Exception as e:
                print(f"Failed to connect to Upstash Redis: {e}")
                self.redis = None
    
    def _get_session_key(self, session_id: str) -> str:
        """Generate Redis key for session"""
        return f"session:agent_makalah:{session_id}"
    
    def create_session(self, user_id: str, user_data: Dict[str, Any]) -> str:
        """
        Create a new user session
        
        Args:
            user_id: User identifier
            user_data: Additional user data to store in session
            
        Returns:
            str: Session ID
        """
        session_id = str(uuid.uuid4())
        
        session_data = {
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
            "last_accessed": datetime.utcnow().isoformat(),
            "user_data": user_data
        }
        
        if self.redis:
            try:
                key = self._get_session_key(session_id)
                self.redis.setex(
                    key,
                    settings.session_max_age,
                    json.dumps(session_data)
                )
            except Exception as e:
                print(f"Failed to create session in Redis: {e}")
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve session data
        
        Args:
            session_id: Session identifier
            
        Returns:
            Optional[Dict[str, Any]]: Session data if found, None otherwise
        """
        if not self.redis:
            return None
        
        try:
            key = self._get_session_key(session_id)
            session_data = self.redis.get(key)
            
            if session_data:
                data = json.loads(session_data)
                # Update last accessed time
                data["last_accessed"] = datetime.utcnow().isoformat()
                self.redis.setex(
                    key,
                    settings.session_max_age,
                    json.dumps(data)
                )
                return data
        except Exception as e:
            print(f"Failed to get session from Redis: {e}")
        
        return None
    
    def update_session(self, session_id: str, user_data: Dict[str, Any]) -> bool:
        """
        Update session data
        
        Args:
            session_id: Session identifier
            user_data: Updated user data
            
        Returns:
            bool: True if session updated successfully, False otherwise
        """
        if not self.redis:
            return False
        
        try:
            key = self._get_session_key(session_id)
            session_data = self.redis.get(key)
            
            if session_data:
                data = json.loads(session_data)
                data["user_data"].update(user_data)
                data["last_accessed"] = datetime.utcnow().isoformat()
                
                self.redis.setex(
                    key,
                    settings.session_max_age,
                    json.dumps(data)
                )
                return True
        except Exception as e:
            print(f"Failed to update session in Redis: {e}")
        
        return False
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            bool: True if session deleted successfully, False otherwise
        """
        if not self.redis:
            return False
        
        try:
            key = self._get_session_key(session_id)
            result = self.redis.delete(key)
            return result == 1
        except Exception as e:
            print(f"Failed to delete session from Redis: {e}")
            return False
    
    def is_session_valid(self, session_id: str) -> bool:
        """
        Check if a session is valid and not expired
        
        Args:
            session_id: Session identifier
            
        Returns:
            bool: True if session is valid, False otherwise
        """
        session_data = self.get_session(session_id)
        return session_data is not None
    
    def get_user_id_from_session(self, session_id: str) -> Optional[str]:
        """
        Get user ID from session
        
        Args:
            session_id: Session identifier
            
        Returns:
            Optional[str]: User ID if session exists, None otherwise
        """
        session_data = self.get_session(session_id)
        if session_data:
            return session_data.get("user_id")
        return None
    
    def cleanup_expired_sessions(self) -> int:
        """
        Clean up expired sessions (Redis handles this automatically with TTL)
        This method is for compatibility and monitoring
        
        Returns:
            int: Number of sessions cleaned up (always 0 as Redis handles TTL)
        """
        # Redis automatically handles TTL expiration
        # This method exists for compatibility with other session stores
        return 0


# Global session manager instance
session_manager = SessionManager() 