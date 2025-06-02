"""
Authentication Middleware for Agent-Makalah Backend
Implements role-based access control and global authentication checks
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable, Set, Optional
import logging
from src.auth.jwt_utils import validate_and_decode_token
from src.crud.crud_user import UserCRUD

logger = logging.getLogger(__name__)


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """
    Global authentication middleware with role-based access control
    Handles authentication for protected routes and enforces user permissions
    """
    
    def __init__(self, app):
        super().__init__(app)
        self.user_crud = UserCRUD()
        
        # Public endpoints that don't require authentication
        self.public_endpoints: Set[str] = {
            "/",
            "/health",
            "/docs",
            "/redoc", 
            "/openapi.json",
            "/api/v1/auth/register",
            "/api/v1/auth/login"
        }
        
        # Endpoints that require superuser access
        self.superuser_endpoints: Set[str] = {
            "/api/v1/admin/",
            "/api/v1/users/",
            "/api/v1/system/",
            "/api/v1/manage/"
        }
        
        # Authentication optional endpoints (provide different response if authenticated)
        self.optional_auth_endpoints: Set[str] = {
            "/api/v1/public/"
        }
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Apply authentication and authorization logic
        
        Args:
            request: Incoming HTTP request
            call_next: Next middleware/handler in chain
            
        Returns:
            Response or authentication error
        """
        path = request.url.path
        
        # Extract and validate token for all requests
        token = self._extract_token(request)
        user_data = None
        
        if token:
            user_data = await self._validate_token_and_get_user(token)
        
        # Skip authentication checks for public endpoints
        if self._is_public_endpoint(path):
            # Add user data to request state anyway (might be useful)
            if user_data:
                request.state.current_user = user_data
                request.state.is_authenticated = True
            else:
                request.state.current_user = None
                request.state.is_authenticated = False
            
            # Continue to next middleware/handler
            response = await call_next(request)
            
            # Add authentication info to response headers
            self._add_auth_headers(response, user_data)
            
            return response
        
        # Check if authentication is required
        if self._requires_authentication(path):
            if not user_data:
                return self._create_auth_error("Authentication required")
            
            # Check superuser access
            if self._requires_superuser(path):
                if not user_data.get("is_superuser", False):
                    return self._create_auth_error("Superuser access required", status.HTTP_403_FORBIDDEN)
        
        # Add user data to request state for use in endpoints
        if user_data:
            request.state.current_user = user_data
            request.state.is_authenticated = True
        else:
            request.state.current_user = None
            request.state.is_authenticated = False
        
        # Continue to next middleware/handler
        response = await call_next(request)
        
        # Add authentication info to response headers
        self._add_auth_headers(response, user_data)
        
        return response
    
    def _extract_token(self, request: Request) -> Optional[str]:
        """
        Extract JWT token from request headers
        
        Args:
            request: HTTP request
            
        Returns:
            Optional[str]: JWT token if found
        """
        # Check Authorization header (Bearer token)
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header[7:]  # Remove "Bearer " prefix
        
        # Check X-API-Key header (alternative)
        api_key = request.headers.get("X-API-Key")
        if api_key:
            return api_key
        
        # Check query parameter (less secure, only for specific endpoints)
        if request.url.path in ["/docs", "/redoc"]:
            return request.query_params.get("token")
        
        return None
    
    async def _validate_token_and_get_user(self, token: str) -> Optional[dict]:
        """
        Validate JWT token and return user data
        
        Args:
            token: JWT token string
            
        Returns:
            Optional[dict]: User data if token is valid
        """
        try:
            # Validate token structure and blacklist
            token_payload = validate_and_decode_token(token, check_blacklist=True)
            if not token_payload:
                return None
            
            # Extract user ID
            user_id = token_payload.get("sub")
            if not user_id:
                return None
            
            # Get user from database
            user = await self.user_crud.get_user_by_id(user_id)
            if not user or not user.is_active:
                return None
            
            # Return user data
            return {
                "user_id": str(user.id),
                "email": user.email,
                "is_active": user.is_active,
                "is_superuser": user.is_superuser,
                "created_at": user.created_at.isoformat(),
                "token_payload": token_payload
            }
            
        except Exception as e:
            logger.warning(f"Token validation failed: {str(e)}")
            return None
    
    def _is_public_endpoint(self, path: str) -> bool:
        """
        Check if endpoint is public (no authentication required)
        
        Args:
            path: Request path
            
        Returns:
            bool: True if endpoint is public
        """
        # Exact match
        if path in self.public_endpoints:
            return True
        
        # Pattern matching for public paths
        public_patterns = [
            "/static/",
            "/favicon.ico",
            "/robots.txt"
        ]
        
        return any(pattern in path for pattern in public_patterns)
    
    def _requires_authentication(self, path: str) -> bool:
        """
        Check if endpoint requires authentication
        
        Args:
            path: Request path
            
        Returns:
            bool: True if authentication is required
        """
        # Public endpoints don't require auth
        if self._is_public_endpoint(path):
            return False
        
        # Optional auth endpoints don't require auth but benefit from it
        if any(pattern in path for pattern in self.optional_auth_endpoints):
            return False
        
        # All other endpoints require authentication
        return True
    
    def _requires_superuser(self, path: str) -> bool:
        """
        Check if endpoint requires superuser access
        
        Args:
            path: Request path
            
        Returns:
            bool: True if superuser access is required
        """
        return any(pattern in path for pattern in self.superuser_endpoints)
    
    def _create_auth_error(self, message: str, status_code: int = status.HTTP_401_UNAUTHORIZED) -> JSONResponse:
        """
        Create authentication error response
        
        Args:
            message: Error message
            status_code: HTTP status code
            
        Returns:
            JSONResponse: Authentication error response
        """
        headers = {"WWW-Authenticate": "Bearer"}
        
        if status_code == status.HTTP_401_UNAUTHORIZED:
            headers["WWW-Authenticate"] = "Bearer"
        
        return JSONResponse(
            status_code=status_code,
            content={
                "error": "Authentication failed",
                "message": message,
                "status_code": status_code
            },
            headers=headers
        )
    
    def _add_auth_headers(self, response: Response, user_data: Optional[dict]) -> None:
        """
        Add authentication information to response headers
        
        Args:
            response: HTTP response
            user_data: User data if authenticated
        """
        if user_data:
            response.headers["X-User-Authenticated"] = "true"
            response.headers["X-User-ID"] = user_data["user_id"]
            response.headers["X-User-Role"] = "superuser" if user_data["is_superuser"] else "user"
        else:
            response.headers["X-User-Authenticated"] = "false"
        
        response.headers["X-Auth-Version"] = "1.0" 