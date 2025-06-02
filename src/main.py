"""
Agent-Makalah Backend System
Main FastAPI application entry point

This is the core FastAPI application for the Agent-Makalah academic writing assistant.
It provides RESTful APIs for the multi-agent system that helps users create and analyze
academic papers in Bahasa Indonesia.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from typing import Dict, Any
import os
from datetime import datetime

# Import API routes
from src.api.routes import api_router
from src.api.auth_routes import auth_router

# Import security middleware
from src.middleware.security_headers import SecurityHeadersMiddleware
from src.middleware.rate_limiting import RateLimitingMiddleware
from src.middleware.auth_middleware import AuthenticationMiddleware
from src.middleware.request_logging import RequestLoggingMiddleware

# Import configuration
from src.core.config import settings

# Initialize FastAPI app
app = FastAPI(
    title="Agent-Makalah Backend API",
    description="AI-powered academic writing assistant for Bahasa Indonesia",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# === MIDDLEWARE CONFIGURATION (Order matters!) ===

# 1. Request Logging Middleware (first to capture all requests)
app.add_middleware(
    RequestLoggingMiddleware,
    log_body=False  # Set to True in development if needed, False in production for security
)

# 2. Security Headers Middleware (early for all responses)
app.add_middleware(
    SecurityHeadersMiddleware,
    environment=settings.environment
)

# 3. Rate Limiting Middleware (before authentication to prevent abuse)
app.add_middleware(RateLimitingMiddleware)

# 4. Authentication Middleware (after rate limiting, before routes)
app.add_middleware(AuthenticationMiddleware)

# 5. CORS Middleware (after auth, allows cross-origin for authenticated requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins if settings.environment == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time", "X-RateLimit-Remaining"]
)

# === ROUTE CONFIGURATION ===

# Include API routes
app.include_router(api_router)
app.include_router(auth_router, prefix="/api/v1")

# Health check response model
class HealthResponse(BaseModel):
    status: str
    message: str
    timestamp: str
    version: str
    system: str
    environment: str
    security_features: Dict[str, bool]


# === CORE ENDPOINTS ===

@app.get("/", response_model=Dict[str, Any])
async def root():
    """
    Root endpoint - basic API information
    """
    return {
        "message": "Agent-Makalah Backend API",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Comprehensive health check endpoint
    """
    return HealthResponse(
        status="healthy",
        message="Agent-Makalah Backend is running",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
        system="Agent-Makalah Backend",
        environment=settings.environment,
        security_features={
            "authentication": True,
            "rate_limiting": True,
            "security_headers": True,
            "request_logging": True,
            "cors_configured": True,
            "jwt_tokens": True,
            "role_based_access": True
        }
    )


@app.get("/security-status")
async def security_status():
    """
    Security status endpoint (requires authentication)
    """
    return {
        "security_status": "active",
        "features": {
            "middleware": {
                "security_headers": "enabled",
                "rate_limiting": "enabled", 
                "authentication": "enabled",
                "request_logging": "enabled"
            },
            "authentication": {
                "jwt_tokens": "enabled",
                "token_blacklisting": "enabled",
                "session_management": "enabled",
                "role_based_access": "enabled"
            },
            "security_headers": {
                "csp": "enabled",
                "xss_protection": "enabled",
                "frame_options": "enabled",
                "content_type_options": "enabled",
                "hsts": "production_only"
            },
            "rate_limiting": {
                "auth_endpoints": "strict",
                "api_endpoints": "moderate",
                "docs_endpoints": "generous"
            }
        },
        "environment": settings.environment,
        "timestamp": datetime.utcnow().isoformat()
    }


# === ERROR HANDLERS ===

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Custom HTTP exception handler with security headers
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        },
        headers={
            "X-Error-Type": "HTTPException",
            "X-Agent-Makalah-Error": "true"
        }
    )


@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    """
    Internal server error handler
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat()
        },
        headers={
            "X-Error-Type": "InternalServerError", 
            "X-Agent-Makalah-Error": "true"
        }
    )


# === APPLICATION STARTUP/SHUTDOWN ===

@app.on_event("startup")
async def startup_event():
    """
    Application startup event
    """
    print("🚀 Agent-Makalah Backend starting up...")
    print(f"📊 Environment: {settings.environment}")
    print("🛡️ Security middleware enabled:")
    print("   - Security Headers ✅")
    print("   - Rate Limiting ✅") 
    print("   - Authentication ✅")
    print("   - Request Logging ✅")
    print("   - CORS Protection ✅")
    print("🔐 Authentication features:")
    print("   - JWT Tokens ✅")
    print("   - Token Blacklisting ✅")
    print("   - Session Management ✅")
    print("   - Role-based Access ✅")
    print("✅ Agent-Makalah Backend ready!")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event
    """
    print("🛑 Agent-Makalah Backend shutting down...")
    print("✅ Cleanup completed")


# === DEVELOPMENT SERVER ===

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        log_level=settings.log_level
    ) 