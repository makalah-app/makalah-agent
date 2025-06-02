"""
Security Headers Middleware for Agent-Makalah Backend
Implements comprehensive security headers to protect against common web vulnerabilities
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response as StarletteResponse
from typing import Callable
import time


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add comprehensive security headers to all HTTP responses
    Protects against XSS, clickjacking, CSRF, and other web vulnerabilities
    """
    
    def __init__(self, app, environment: str = "development"):
        super().__init__(app)
        self.environment = environment
        self.is_production = environment == "production"
    
    async def dispatch(self, request: Request, call_next: Callable) -> StarletteResponse:
        """
        Add security headers to all responses
        
        Args:
            request: Incoming HTTP request
            call_next: Next middleware/handler in chain
            
        Returns:
            Response with security headers added
        """
        # Process request
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Add comprehensive security headers
        self._add_security_headers(response, request)
        
        # Add performance header
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
    
    def _add_security_headers(self, response: Response, request: Request) -> None:
        """
        Add all security headers to the response
        
        Args:
            response: HTTP response object
            request: HTTP request object
        """
        # Content Security Policy (CSP)
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'",  # Relaxed for FastAPI docs
            "style-src 'self' 'unsafe-inline'",  # Relaxed for FastAPI docs  
            "img-src 'self' data: https:",
            "font-src 'self'",
            "connect-src 'self'",
            "frame-ancestors 'none'",
            "form-action 'self'",
            "base-uri 'self'"
        ]
        response.headers["Content-Security-Policy"] = "; ".join(csp_directives)
        
        # XSS Protection
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # Prevent MIME sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # Clickjacking protection  
        response.headers["X-Frame-Options"] = "DENY"
        
        # Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Permissions Policy (Feature Policy replacement)
        permissions_policy = [
            "geolocation=()",
            "microphone=()",
            "camera=()",
            "payment=()",
            "usb=()",
            "magnetometer=()",
            "gyroscope=()",
            "speaker=()"
        ]
        response.headers["Permissions-Policy"] = ", ".join(permissions_policy)
        
        # HSTS (HTTP Strict Transport Security) - only in production with HTTPS
        if self.is_production:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Server information hiding
        response.headers["Server"] = "Agent-Makalah"
        
        # Cache control for sensitive endpoints
        if self._is_sensitive_endpoint(request.url.path):
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        
        # Custom Agent-Makalah headers
        response.headers["X-Agent-Makalah-Version"] = "1.0.0"
        response.headers["X-API-Version"] = "v1"
    
    def _is_sensitive_endpoint(self, path: str) -> bool:
        """
        Check if endpoint contains sensitive data that shouldn't be cached
        
        Args:
            path: Request path
            
        Returns:
            bool: True if endpoint is sensitive
        """
        sensitive_patterns = [
            "/api/v1/auth/",
            "/api/v1/user/",
            "/api/v1/profile/",
            "/api/v1/session/",
            "/api/v1/admin/"
        ]
        
        return any(pattern in path for pattern in sensitive_patterns) 