"""
Enhanced Session Management for Agent-Makalah
Comprehensive session management integrating JWT tokens, Redis storage, and token blacklisting
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple, List
from upstash_redis import Redis
from src.core.config import settings
from src.auth.jwt_utils import create_token_pair, validate_and_decode_token, get_user_id_from_token
from src.auth.token_blacklist import token_blacklist


class EnhancedSessionManager:
    """
    Enhanced session manager with JWT token integration and blacklisting
    """
    
    def __init__(self):
        """Initialize enhanced session manager with Upstash Redis connection"""
        self.redis = None
        if settings.upstash_redis_url and settings.upstash_redis_token:
            try:
                self.redis = Redis(
                    url=settings.upstash_redis_url,
                    token=settings.upstash_redis_token
                )
            except Exception as e:
                print(f"Failed to connect to Upstash Redis for session: {e}")
                self.redis = None
    
    def _get_session_key(self, session_id: str) -> str:
        """Generate Redis key for session"""
        return f"enhanced_session:agent_makalah:{session_id}"
    
    def _get_user_sessions_key(self, user_id: str) -> str:
        """Generate Redis key for user's active sessions"""
        return f"user_sessions:agent_makalah:{user_id}"
    
    def create_authenticated_session(
        self, 
        user_id: str, 
        user_data: Dict[str, Any],
        device_info: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, str, str]:
        """
        Create comprehensive authenticated session with JWT tokens
        
        Args:
            user_id: User identifier
            user_data: User data to include in JWT tokens
            device_info: Optional device/client information
            
        Returns:
            Tuple[str, str, str]: (session_id, access_token, refresh_token)
        """
        session_id = str(uuid.uuid4())
        
        # Create JWT token pair
        jwt_user_data = {
            "sub": user_id,
            "email": user_data.get("email"),
            "is_superuser": user_data.get("is_superuser", False)
        }
        
        access_token, refresh_token = create_token_pair(jwt_user_data)
        
        # Create session data
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
            "last_accessed": datetime.utcnow().isoformat(),
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_data": user_data,
            "device_info": device_info or {},
            "is_active": True
        }
        
        if self.redis:
            try:
                # Store session
                session_key = self._get_session_key(session_id)
                self.redis.setex(
                    session_key,
                    settings.session_max_age,
                    json.dumps(session_data)
                )
                
                # Track session for user
                user_sessions_key = self._get_user_sessions_key(user_id)
                self.redis.sadd(user_sessions_key, session_id)
                self.redis.expire(user_sessions_key, settings.session_max_age)
                
                # Track tokens in blacklist manager
                token_blacklist.track_user_token(user_id, access_token)
                token_blacklist.track_user_token(user_id, refresh_token)
                
            except Exception as e:
                print(f"Failed to create enhanced session in Redis: {e}")
        
        return session_id, access_token, refresh_token
    
    def get_session_from_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Get session data from JWT token
        
        Args:
            token: JWT access or refresh token
            
        Returns:
            Optional[Dict[str, Any]]: Session data if valid, None otherwise
        """
        # Validate token (includes blacklist check)
        payload = validate_and_decode_token(token)
        if not payload:
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        # Find session containing this token
        if self.redis:
            try:
                user_sessions_key = self._get_user_sessions_key(user_id)
                session_ids = self.redis.smembers(user_sessions_key)
                
                for session_id in session_ids:
                    session_key = self._get_session_key(session_id)
                    session_data = self.redis.get(session_key)
                    
                    if session_data:
                        data = json.loads(session_data)
                        if (data.get("access_token") == token or 
                            data.get("refresh_token") == token):
                            # Update last accessed
                            data["last_accessed"] = datetime.utcnow().isoformat()
                            self.redis.setex(
                                session_key,
                                settings.session_max_age,
                                json.dumps(data)
                            )
                            return data
                            
            except Exception as e:
                print(f"Failed to get session from token: {e}")
        
        return None
    
    def refresh_session_token(self, refresh_token: str) -> Optional[Tuple[str, str]]:
        """
        Refresh access token using refresh token
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            Optional[Tuple[str, str]]: (new_access_token, session_id) if successful, None otherwise
        """
        # Get session from refresh token
        session_data = self.get_session_from_token(refresh_token)
        if not session_data:
            return None
        
        # Verify this is actually a refresh token
        payload = validate_and_decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            return None
        
        user_id = session_data["user_id"]
        session_id = session_data["session_id"]
        
        # Create new access token
        from src.auth.jwt_utils import refresh_access_token
        new_access_token = refresh_access_token(refresh_token)
        if not new_access_token:
            return None
        
        # Update session with new access token
        if self.redis:
            try:
                # Blacklist old access token
                old_access_token = session_data.get("access_token")
                if old_access_token:
                    token_blacklist.blacklist_token(old_access_token, "token_refresh")
                
                # Update session
                session_data["access_token"] = new_access_token
                session_data["last_accessed"] = datetime.utcnow().isoformat()
                
                session_key = self._get_session_key(session_id)
                self.redis.setex(
                    session_key,
                    settings.session_max_age,
                    json.dumps(session_data)
                )
                
                # Track new token
                token_blacklist.track_user_token(user_id, new_access_token)
                
                return new_access_token, session_id
                
            except Exception as e:
                print(f"Failed to refresh session token: {e}")
        
        return None
    
    def logout_session(self, token: str) -> bool:
        """
        Logout a specific session using any valid token
        
        Args:
            token: Access or refresh token from session
            
        Returns:
            bool: True if logout successful, False otherwise
        """
        session_data = self.get_session_from_token(token)
        if not session_data:
            return False
        
        session_id = session_data["session_id"]
        user_id = session_data["user_id"]
        
        if self.redis:
            try:
                # Blacklist both tokens
                access_token = session_data.get("access_token")
                refresh_token = session_data.get("refresh_token")
                
                if access_token:
                    token_blacklist.blacklist_token(access_token, "user_logout")
                if refresh_token:
                    token_blacklist.blacklist_token(refresh_token, "user_logout")
                
                # Remove session
                session_key = self._get_session_key(session_id)
                self.redis.delete(session_key)
                
                # Remove from user sessions
                user_sessions_key = self._get_user_sessions_key(user_id)
                self.redis.srem(user_sessions_key, session_id)
                
                return True
                
            except Exception as e:
                print(f"Failed to logout session: {e}")
        
        return False
    
    def logout_all_user_sessions(self, user_id: str) -> int:
        """
        Logout all sessions for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            int: Number of sessions logged out
        """
        if not self.redis:
            return 0
        
        try:
            # Get all user sessions
            user_sessions_key = self._get_user_sessions_key(user_id)
            session_ids = self.redis.smembers(user_sessions_key)
            
            logged_out_count = 0
            
            for session_id in session_ids:
                try:
                    session_key = self._get_session_key(session_id)
                    session_data = self.redis.get(session_key)
                    
                    if session_data:
                        data = json.loads(session_data)
                        
                        # Blacklist tokens
                        access_token = data.get("access_token")
                        refresh_token = data.get("refresh_token")
                        
                        if access_token:
                            token_blacklist.blacklist_token(access_token, "mass_logout")
                        if refresh_token:
                            token_blacklist.blacklist_token(refresh_token, "mass_logout")
                        
                        # Delete session
                        self.redis.delete(session_key)
                        logged_out_count += 1
                        
                except Exception as e:
                    print(f"Failed to logout session {session_id}: {e}")
            
            # Clear user sessions set
            self.redis.delete(user_sessions_key)
            
            print(f"Logged out {logged_out_count} sessions for user {user_id}")
            return logged_out_count
            
        except Exception as e:
            print(f"Failed to logout all user sessions: {e}")
            return 0
    
    def get_user_active_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get all active sessions for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            List[Dict[str, Any]]: List of active session data
        """
        if not self.redis:
            return []
        
        try:
            user_sessions_key = self._get_user_sessions_key(user_id)
            session_ids = self.redis.smembers(user_sessions_key)
            
            active_sessions = []
            
            for session_id in session_ids:
                session_key = self._get_session_key(session_id)
                session_data = self.redis.get(session_key)
                
                if session_data:
                    data = json.loads(session_data)
                    # Remove sensitive tokens from response
                    safe_data = {
                        "session_id": data.get("session_id"),
                        "created_at": data.get("created_at"),
                        "last_accessed": data.get("last_accessed"),
                        "device_info": data.get("device_info", {}),
                        "is_active": data.get("is_active", True)
                    }
                    active_sessions.append(safe_data)
            
            return active_sessions
            
        except Exception as e:
            print(f"Failed to get user active sessions: {e}")
            return []
    
    def validate_session_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Comprehensive token and session validation
        
        Args:
            token: JWT token to validate
            
        Returns:
            Optional[Dict[str, Any]]: User data if valid, None otherwise
        """
        session_data = self.get_session_from_token(token)
        if not session_data:
            return None
        
        # Return safe user data
        return {
            "user_id": session_data["user_id"],
            "session_id": session_data["session_id"],
            "user_data": session_data["user_data"],
            "last_accessed": session_data["last_accessed"]
        }
    
    def cleanup_expired_sessions(self) -> int:
        """
        Clean up expired sessions (Redis handles TTL automatically)
        This method is for monitoring purposes
        
        Returns:
            int: Number of sessions cleaned up (always 0 as Redis handles TTL)
        """
        # Redis automatically handles TTL expiration
        return 0


# Global enhanced session manager instance
enhanced_session_manager = EnhancedSessionManager() 