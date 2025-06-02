"""
Rate Limiting Middleware for Agent-Makalah Backend
Implements intelligent rate limiting to prevent abuse, brute force attacks, and excessive API usage
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable, Dict, Optional
import time
import hashlib
from collections import defaultdict, deque
from src.core.config import settings


class RateLimitingMiddleware(BaseHTTPMiddleware):
    """
    Advanced rate limiting middleware with different limits for different endpoint types
    Uses in-memory storage with sliding window algorithm
    """
    
    def __init__(self, app):
        super().__init__(app)
        
        # Rate limit configurations (requests per window)
        self.rate_limits = {
            # Authentication endpoints - stricter limits
            "auth_login": {"requests": 5, "window": 300},      # 5 login attempts per 5 minutes
            "auth_register": {"requests": 3, "window": 3600},  # 3 registrations per hour
            "auth_refresh": {"requests": 10, "window": 300},   # 10 token refreshes per 5 minutes
            
            # API endpoints - generous limits 
            "api_general": {"requests": 100, "window": 60},    # 100 requests per minute
            "api_upload": {"requests": 10, "window": 300},     # 10 file uploads per 5 minutes
            
            # Documentation endpoints - very generous
            "docs": {"requests": 50, "window": 60},            # 50 requests per minute
            
            # Default rate limit
            "default": {"requests": 60, "window": 60}          # 60 requests per minute
        }
        
        # Storage for rate limiting data
        # Structure: {client_key: {endpoint_type: deque([timestamp, timestamp, ...])}}
        self.request_history: Dict[str, Dict[str, deque]] = defaultdict(lambda: defaultdict(deque))
        
        # Blacklist for severe violators
        self.blacklist: Dict[str, float] = {}  # {client_key: unblock_timestamp}
        
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Apply rate limiting logic to incoming requests
        
        Args:
            request: Incoming HTTP request
            call_next: Next middleware/handler in chain
            
        Returns:
            Response or 429 Too Many Requests error
        """
        # Get client identifier
        client_key = self._get_client_key(request)
        
        # Check blacklist first
        if self._is_blacklisted(client_key):
            return self._create_rate_limit_response(
                "Client temporarily blacklisted due to excessive violations",
                retry_after=3600  # 1 hour
            )
        
        # Determine endpoint type and rate limit
        endpoint_type = self._get_endpoint_type(request.url.path)
        rate_config = self.rate_limits.get(endpoint_type, self.rate_limits["default"])
        
        # Check rate limit
        if not self._is_request_allowed(client_key, endpoint_type, rate_config):
            # Log violation and check for blacklist conditions
            self._log_violation(client_key, endpoint_type, request)
            
            # Return rate limit exceeded response
            return self._create_rate_limit_response(
                f"Rate limit exceeded for {endpoint_type}",
                retry_after=rate_config["window"]
            )
        
        # Record this request
        self._record_request(client_key, endpoint_type)
        
        # Continue to next middleware/handler
        response = await call_next(request)
        
        # Add rate limit headers to response
        self._add_rate_limit_headers(response, client_key, endpoint_type, rate_config)
        
        return response
    
    def _get_client_key(self, request: Request) -> str:
        """
        Generate unique client identifier for rate limiting
        
        Args:
            request: HTTP request
            
        Returns:
            str: Unique client identifier
        """
        # Primary: Use X-Forwarded-For or X-Real-IP (behind proxy)
        client_ip = (
            request.headers.get("X-Forwarded-For", "").split(",")[0].strip() or
            request.headers.get("X-Real-IP") or
            request.client.host if request.client else "unknown"
        )
        
        # Secondary: Include User-Agent for more granular control
        user_agent = request.headers.get("User-Agent", "")
        
        # Create hash for consistent key length
        key_data = f"{client_ip}:{user_agent}"
        return hashlib.md5(key_data.encode()).hexdigest()[:16]
    
    def _get_endpoint_type(self, path: str) -> str:
        """
        Classify endpoint type for rate limiting rules
        
        Args:
            path: Request path
            
        Returns:
            str: Endpoint type classification
        """
        # Authentication endpoints
        if "/auth/login" in path:
            return "auth_login"
        elif "/auth/register" in path:
            return "auth_register" 
        elif "/auth/refresh" in path:
            return "auth_refresh"
        elif "/auth/" in path:
            return "auth_general"
        
        # File upload endpoints
        elif "/upload" in path or "/file" in path:
            return "api_upload"
        
        # Documentation endpoints
        elif path in ["/docs", "/redoc", "/openapi.json"]:
            return "docs"
        
        # API endpoints
        elif "/api/" in path:
            return "api_general"
        
        # Default
        return "default"
    
    def _is_request_allowed(self, client_key: str, endpoint_type: str, rate_config: Dict) -> bool:
        """
        Check if request is allowed based on rate limits
        
        Args:
            client_key: Client identifier
            endpoint_type: Type of endpoint
            rate_config: Rate limit configuration
            
        Returns:
            bool: True if request is allowed
        """
        current_time = time.time()
        window_start = current_time - rate_config["window"]
        
        # Get request history for this client and endpoint
        request_queue = self.request_history[client_key][endpoint_type]
        
        # Clean old requests outside the window
        while request_queue and request_queue[0] < window_start:
            request_queue.popleft()
        
        # Check if within limit
        return len(request_queue) < rate_config["requests"]
    
    def _record_request(self, client_key: str, endpoint_type: str) -> None:
        """
        Record a request in the rate limiting history
        
        Args:
            client_key: Client identifier
            endpoint_type: Type of endpoint
        """
        current_time = time.time()
        self.request_history[client_key][endpoint_type].append(current_time)
    
    def _log_violation(self, client_key: str, endpoint_type: str, request: Request) -> None:
        """
        Log rate limit violation and handle blacklisting
        
        Args:
            client_key: Client identifier
            endpoint_type: Type of endpoint
            request: HTTP request
        """
        print(f"Rate limit violation: {client_key} exceeded {endpoint_type} limit from {request.client.host if request.client else 'unknown'}")
        
        # Check for blacklist conditions (multiple violations across different endpoints)
        total_violations = sum(
            len(queue) for queue in self.request_history[client_key].values()
        )
        
        # Blacklist if too many violations across different endpoints
        if total_violations > 500:  # Threshold for blacklisting
            self.blacklist[client_key] = time.time() + 3600  # Block for 1 hour
            print(f"Blacklisted client: {client_key} for 1 hour due to excessive violations")
    
    def _is_blacklisted(self, client_key: str) -> bool:
        """
        Check if client is blacklisted
        
        Args:
            client_key: Client identifier
            
        Returns:
            bool: True if client is blacklisted
        """
        if client_key in self.blacklist:
            if time.time() > self.blacklist[client_key]:
                # Unblock expired blacklist
                del self.blacklist[client_key]
                return False
            return True
        return False
    
    def _create_rate_limit_response(self, message: str, retry_after: int) -> JSONResponse:
        """
        Create rate limit exceeded response
        
        Args:
            message: Error message
            retry_after: Seconds to wait before retrying
            
        Returns:
            JSONResponse: 429 error response
        """
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "error": "Rate limit exceeded",
                "message": message,
                "retry_after": retry_after,
                "timestamp": time.time()
            },
            headers={
                "Retry-After": str(retry_after),
                "X-RateLimit-Exceeded": "true"
            }
        )
    
    def _add_rate_limit_headers(
        self, 
        response: Response, 
        client_key: str, 
        endpoint_type: str, 
        rate_config: Dict
    ) -> None:
        """
        Add rate limit information headers to response
        
        Args:
            response: HTTP response
            client_key: Client identifier
            endpoint_type: Type of endpoint
            rate_config: Rate limit configuration
        """
        # Calculate remaining requests
        current_requests = len(self.request_history[client_key][endpoint_type])
        remaining = max(0, rate_config["requests"] - current_requests)
        
        # Add headers
        response.headers["X-RateLimit-Limit"] = str(rate_config["requests"])
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Window"] = str(rate_config["window"])
        response.headers["X-RateLimit-Type"] = endpoint_type
    
    def cleanup_old_data(self) -> None:
        """
        Cleanup old rate limiting data to prevent memory leaks
        Should be called periodically by a background task
        """
        current_time = time.time()
        
        # Clean request history
        for client_key in list(self.request_history.keys()):
            for endpoint_type in list(self.request_history[client_key].keys()):
                queue = self.request_history[client_key][endpoint_type]
                # Remove requests older than 1 hour
                while queue and queue[0] < current_time - 3600:
                    queue.popleft()
                
                # Remove empty queues
                if not queue:
                    del self.request_history[client_key][endpoint_type]
            
            # Remove empty client records
            if not self.request_history[client_key]:
                del self.request_history[client_key]
        
        # Clean expired blacklist entries
        for client_key in list(self.blacklist.keys()):
            if current_time > self.blacklist[client_key]:
                del self.blacklist[client_key] 