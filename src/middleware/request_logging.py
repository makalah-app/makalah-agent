"""
Request Logging Middleware for Agent-Makalah Backend
Implements comprehensive request logging for security monitoring and performance tracking
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable
import time
import json
import logging
from datetime import datetime
import uuid

# Setup logging for security events
security_logger = logging.getLogger("agent_makalah.security")
performance_logger = logging.getLogger("agent_makalah.performance")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Comprehensive request logging middleware for security monitoring and performance tracking
    Logs authentication events, suspicious activities, and performance metrics
    """
    
    def __init__(self, app, log_body: bool = False):
        super().__init__(app)
        self.log_body = log_body  # Whether to log request/response bodies (security consideration)
        
        # Security-sensitive endpoints to monitor closely
        self.security_endpoints = [
            "/api/v1/auth/",
            "/api/v1/admin/",
            "/api/v1/user/",
            "/api/v1/profile/",
            "/api/v1/session/"
        ]
        
        # Performance-critical endpoints to monitor
        self.performance_endpoints = [
            "/api/v1/upload/",
            "/api/v1/process/",
            "/api/v1/generate/",
            "/api/v1/agent/"
        ]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Log request and response information for monitoring
        
        Args:
            request: Incoming HTTP request
            call_next: Next middleware/handler in chain
            
        Returns:
            Response with logging applied
        """
        # Generate request ID for tracking
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id
        
        # Record request start time
        start_time = time.time()
        
        # Extract request information
        request_info = await self._extract_request_info(request, request_id)
        
        # Log incoming request
        self._log_request(request_info)
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Extract response information
            response_info = self._extract_response_info(response, response_time, request_id)
            
            # Log response
            self._log_response(request_info, response_info)
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            
            return response
            
        except Exception as e:
            # Log error
            error_time = time.time() - start_time
            self._log_error(request_info, str(e), error_time)
            raise
    
    async def _extract_request_info(self, request: Request, request_id: str) -> dict:
        """
        Extract comprehensive request information for logging
        
        Args:
            request: HTTP request
            request_id: Unique request identifier
            
        Returns:
            dict: Request information
        """
        # Get client information
        client_ip = (
            request.headers.get("X-Forwarded-For", "").split(",")[0].strip() or
            request.headers.get("X-Real-IP") or
            request.client.host if request.client else "unknown"
        )
        
        # Extract user agent and other headers
        user_agent = request.headers.get("User-Agent", "")
        authorization = request.headers.get("Authorization", "")
        content_type = request.headers.get("Content-Type", "")
        
        # Request body (if configured to log)
        body = None
        if self.log_body and content_type.startswith("application/json"):
            try:
                body = await request.body()
                if body:
                    body = body.decode("utf-8")[:1000]  # Limit body size
            except:
                body = "<failed_to_read>"
        
        return {
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat(),
            "method": request.method,
            "path": str(request.url.path),
            "query_params": dict(request.query_params),
            "client_ip": client_ip,
            "user_agent": user_agent,
            "has_authorization": bool(authorization),
            "content_type": content_type,
            "content_length": request.headers.get("Content-Length"),
            "body": body,
            "headers": {
                k: v for k, v in request.headers.items() 
                if k.lower() not in ["authorization", "cookie"]  # Exclude sensitive headers
            }
        }
    
    def _extract_response_info(self, response: Response, response_time: float, request_id: str) -> dict:
        """
        Extract response information for logging
        
        Args:
            response: HTTP response
            response_time: Response processing time
            request_id: Request identifier
            
        Returns:
            dict: Response information
        """
        return {
            "request_id": request_id,
            "status_code": response.status_code,
            "response_time": round(response_time, 4),
            "content_type": response.headers.get("Content-Type", ""),
            "content_length": response.headers.get("Content-Length"),
            "headers": {
                k: v for k, v in response.headers.items()
                if k.lower() not in ["set-cookie"]  # Exclude sensitive headers
            }
        }
    
    def _log_request(self, request_info: dict) -> None:
        """
        Log incoming request with appropriate level based on endpoint sensitivity
        
        Args:
            request_info: Request information dictionary
        """
        path = request_info["path"]
        method = request_info["method"]
        client_ip = request_info["client_ip"]
        request_id = request_info["request_id"]
        
        # Determine log level and logger based on endpoint type
        is_security_endpoint = any(pattern in path for pattern in self.security_endpoints)
        is_performance_endpoint = any(pattern in path for pattern in self.performance_endpoints)
        
        # Create log message
        log_message = f"[{request_id}] {method} {path} from {client_ip}"
        
        # Security endpoint logging
        if is_security_endpoint:
            security_logger.info(log_message, extra={
                "event_type": "security_request",
                "request_info": request_info
            })
            
            # Special handling for authentication endpoints
            if "/auth/" in path:
                if method == "POST" and "/login" in path:
                    security_logger.info(f"[{request_id}] Login attempt from {client_ip}")
                elif method == "POST" and "/register" in path:
                    security_logger.info(f"[{request_id}] Registration attempt from {client_ip}")
                elif "/logout" in path:
                    security_logger.info(f"[{request_id}] Logout from {client_ip}")
        
        # Performance endpoint logging
        elif is_performance_endpoint:
            performance_logger.info(log_message, extra={
                "event_type": "performance_request",
                "request_info": request_info
            })
        
        # General endpoint logging (debug level)
        else:
            logging.debug(log_message, extra={
                "event_type": "general_request",
                "request_info": request_info
            })
    
    def _log_response(self, request_info: dict, response_info: dict) -> None:
        """
        Log response information with security and performance analysis
        
        Args:
            request_info: Request information
            response_info: Response information
        """
        path = request_info["path"]
        status_code = response_info["status_code"]
        response_time = response_info["response_time"]
        request_id = response_info["request_id"]
        client_ip = request_info["client_ip"]
        
        # Create response message
        log_message = f"[{request_id}] {status_code} in {response_time}s"
        
        # Security analysis
        if any(pattern in path for pattern in self.security_endpoints):
            # Log security events
            if status_code == 401:
                security_logger.warning(f"[{request_id}] Authentication failed from {client_ip} to {path}")
            elif status_code == 403:
                security_logger.warning(f"[{request_id}] Authorization denied from {client_ip} to {path}")
            elif status_code == 429:
                security_logger.warning(f"[{request_id}] Rate limit exceeded from {client_ip} to {path}")
            elif "/auth/login" in path and status_code == 200:
                security_logger.info(f"[{request_id}] Successful login from {client_ip}")
            elif "/auth/register" in path and status_code == 201:
                security_logger.info(f"[{request_id}] Successful registration from {client_ip}")
            
            # Log to security logger
            security_logger.info(log_message, extra={
                "event_type": "security_response",
                "request_info": request_info,
                "response_info": response_info
            })
        
        # Performance analysis
        if any(pattern in path for pattern in self.performance_endpoints):
            # Log slow requests
            if response_time > 5.0:  # Requests taking more than 5 seconds
                performance_logger.warning(f"[{request_id}] Slow response: {response_time}s for {path}")
            elif response_time > 2.0:  # Requests taking more than 2 seconds
                performance_logger.info(f"[{request_id}] Medium response time: {response_time}s for {path}")
            
            # Log to performance logger
            performance_logger.info(log_message, extra={
                "event_type": "performance_response",
                "request_info": request_info,
                "response_info": response_info
            })
        
        # Server errors
        if status_code >= 500:
            logging.error(f"[{request_id}] Server error {status_code} for {path} from {client_ip}")
        
        # Client errors (excluding expected auth failures)
        elif status_code >= 400 and status_code not in [401, 403, 404, 429]:
            logging.warning(f"[{request_id}] Client error {status_code} for {path} from {client_ip}")
    
    def _log_error(self, request_info: dict, error: str, error_time: float) -> None:
        """
        Log request processing errors
        
        Args:
            request_info: Request information
            error: Error message
            error_time: Time until error occurred
        """
        request_id = request_info["request_id"]
        path = request_info["path"]
        client_ip = request_info["client_ip"]
        
        error_message = f"[{request_id}] Request error after {error_time:.4f}s: {error}"
        
        logging.error(error_message, extra={
            "event_type": "request_error",
            "request_info": request_info,
            "error": error,
            "error_time": error_time
        })
        
        # Security logger for security endpoints
        if any(pattern in path for pattern in self.security_endpoints):
            security_logger.error(f"[{request_id}] Security endpoint error: {error} from {client_ip}")
    
    def get_security_stats(self) -> dict:
        """
        Get security statistics for monitoring
        This would typically integrate with monitoring systems
        
        Returns:
            dict: Security statistics
        """
        # This is a placeholder for actual metrics collection
        return {
            "message": "Security statistics would be collected here",
            "timestamp": datetime.utcnow().isoformat()
        } 