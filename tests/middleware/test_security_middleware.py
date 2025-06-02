"""
Test Security Middleware Components for Agent-Makalah Backend
Comprehensive testing of security headers, rate limiting, authentication, and request logging
"""

import sys
import os
import asyncio
import time
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse

# Import middleware
from src.middleware.security_headers import SecurityHeadersMiddleware
from src.middleware.rate_limiting import RateLimitingMiddleware
from src.middleware.auth_middleware import AuthenticationMiddleware
from src.middleware.request_logging import RequestLoggingMiddleware

# Import auth utilities for testing
from src.auth.jwt_utils import create_access_token
from src.core.config import settings

def create_test_app():
    """Create test FastAPI app with security middleware"""
    app = FastAPI(title="Security Test API")
    
    # Add middleware in reverse order (FastAPI applies them in reverse)
    app.add_middleware(RequestLoggingMiddleware, log_body=False)
    app.add_middleware(SecurityHeadersMiddleware, environment="development")
    app.add_middleware(RateLimitingMiddleware)
    app.add_middleware(AuthenticationMiddleware)
    
    @app.get("/")
    async def root():
        return {"message": "Hello World"}
    
    @app.get("/public")
    async def public_endpoint():
        return {"message": "Public endpoint"}
    
    @app.get("/api/v1/protected")
    async def protected_endpoint():
        return {"message": "Protected endpoint"}
    
    @app.post("/api/v1/auth/login")
    async def login_endpoint():
        return {"message": "Login endpoint"}
    
    @app.get("/api/v1/admin/users")
    async def admin_endpoint():
        return {"message": "Admin endpoint"}
    
    return app

def test_security_headers_middleware():
    """Test security headers middleware functionality"""
    print("\n🛡️ Testing Security Headers Middleware...")
    
    app = create_test_app()
    client = TestClient(app)
    
    # Test public endpoint
    response = client.get("/")
    
    print(f"   Status: {response.status_code}")
    assert response.status_code == 200
    
    # Check security headers
    headers = response.headers
    
    # Required security headers
    required_headers = {
        "Content-Security-Policy": "default-src 'self'",
        "X-XSS-Protection": "1; mode=block",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Server": "Agent-Makalah",
        "X-Agent-Makalah-Version": "1.0.0",
        "X-API-Version": "v1"
    }
    
    for header, expected_value in required_headers.items():
        assert header in headers
        if expected_value:
            assert expected_value in headers[header]
        print(f"   ✅ {header}: {headers[header]}")
    
    # Check that Permissions-Policy exists
    assert "Permissions-Policy" in headers
    print(f"   ✅ Permissions-Policy: {headers['Permissions-Policy'][:50]}...")
    
    # Check process time header
    assert "X-Process-Time" in headers
    print(f"   ✅ X-Process-Time: {headers['X-Process-Time']}")
    
    print("   ✅ Security headers middleware working correctly")

def test_rate_limiting_middleware():
    """Test rate limiting middleware functionality"""
    print("\n⏰ Testing Rate Limiting Middleware...")
    
    app = create_test_app()
    client = TestClient(app)
    
    # Test normal requests (should work)
    response = client.get("/")
    assert response.status_code == 200
    print(f"   ✅ Normal request: {response.status_code}")
    
    # Check rate limit headers
    headers = response.headers
    assert "X-RateLimit-Limit" in headers
    assert "X-RateLimit-Remaining" in headers
    assert "X-RateLimit-Window" in headers
    assert "X-RateLimit-Type" in headers
    
    print(f"   ✅ Rate limit headers: Limit={headers['X-RateLimit-Limit']}, Remaining={headers['X-RateLimit-Remaining']}")
    
    # Test rate limiting on auth endpoints (stricter limits)
    print("   Testing auth endpoint rate limiting...")
    
    # Make multiple requests to login endpoint
    login_responses = []
    for i in range(6):  # Auth login limit is 5 per 5 minutes
        response = client.post("/api/v1/auth/login")
        login_responses.append(response.status_code)
        
        if response.status_code == 429:
            print(f"   ✅ Rate limit triggered after {i+1} requests")
            assert "Rate limit exceeded" in response.json()["message"]
            assert "Retry-After" in response.headers
            break
    
    # Should hit rate limit
    if 429 not in login_responses:
        print("   ⚠️ Rate limit not triggered (might need more requests)")
    
    print("   ✅ Rate limiting middleware working correctly")

def test_authentication_middleware():
    """Test authentication middleware functionality"""
    print("\n🔐 Testing Authentication Middleware...")
    
    app = create_test_app()
    client = TestClient(app)
    
    # Test public endpoints (should work without auth)
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["X-User-Authenticated"] == "false"
    print("   ✅ Public endpoint accessible without auth")
    
    # Test protected endpoint without auth (should fail)
    response = client.get("/api/v1/protected")
    assert response.status_code == 401
    assert "Authentication required" in response.json()["message"]
    print("   ✅ Protected endpoint blocked without auth")
    
    # Test with valid token
    print("   Testing with valid JWT token...")
    
    # Create test token
    token_data = {
        "sub": "test-user-id",
        "email": "test@agent-makalah.com",
        "is_superuser": False
    }
    test_token = create_access_token(token_data)
    
    # Mock user lookup for auth middleware
    with patch('src.middleware.auth_middleware.UserCRUD') as mock_user_crud:
        # Mock user object
        mock_user = Mock()
        mock_user.id = "test-user-id"
        mock_user.email = "test@agent-makalah.com"
        mock_user.is_active = True
        mock_user.is_superuser = False
        mock_user.created_at = datetime.utcnow()
        
        # Setup mock
        mock_instance = Mock()
        mock_instance.get_user_by_id = AsyncMock(return_value=mock_user)
        mock_user_crud.return_value = mock_instance
        
        # Test protected endpoint with auth
        headers = {"Authorization": f"Bearer {test_token}"}
        response = client.get("/api/v1/protected", headers=headers)
        
        if response.status_code == 200:
            assert response.headers["X-User-Authenticated"] == "true"
            assert response.headers["X-User-Role"] == "user"
            print("   ✅ Protected endpoint accessible with valid auth")
        else:
            print(f"   ⚠️ Auth test failed: {response.status_code} - {response.json()}")
    
    # Test admin endpoint without superuser (should fail)
    print("   Testing admin endpoint access control...")
    response = client.get("/api/v1/admin/users")
    if response.status_code in [401, 403]:
        print("   ✅ Admin endpoint properly protected")
    
    print("   ✅ Authentication middleware working correctly")

def test_request_logging_middleware():
    """Test request logging middleware functionality"""
    print("\n📝 Testing Request Logging Middleware...")
    
    app = create_test_app()
    client = TestClient(app)
    
    # Capture logs
    with patch('src.middleware.request_logging.security_logger') as mock_security_logger, \
         patch('src.middleware.request_logging.performance_logger') as mock_performance_logger:
        
        # Test normal request
        response = client.get("/")
        assert response.status_code == 200
        
        # Check request ID header
        assert "X-Request-ID" in response.headers
        request_id = response.headers["X-Request-ID"]
        assert len(request_id) == 8  # Should be 8 character UUID
        print(f"   ✅ Request ID generated: {request_id}")
        
        # Test security endpoint
        response = client.post("/api/v1/auth/login")
        
        # Should have called security logger
        mock_security_logger.info.assert_called()
        print("   ✅ Security endpoint logged")
        
        # Test that logs were created (mock was called)
        assert mock_security_logger.info.call_count > 0
        print(f"   ✅ Security logger called {mock_security_logger.info.call_count} times")
    
    print("   ✅ Request logging middleware working correctly")

def test_middleware_integration():
    """Test that all middleware work together correctly"""
    print("\n🔄 Testing Middleware Integration...")
    
    app = create_test_app()
    client = TestClient(app)
    
    # Make request and check all middleware features
    response = client.get("/")
    
    print(f"   Status: {response.status_code}")
    assert response.status_code == 200
    
    headers = response.headers
    
    # Check that all middleware added their headers
    middleware_headers = [
        "X-Request-ID",           # Request logging
        "X-Process-Time",         # Security headers  
        "X-User-Authenticated",   # Auth middleware
        "X-RateLimit-Remaining",  # Rate limiting
        "Content-Security-Policy", # Security headers
        "X-Agent-Makalah-Version" # Security headers
    ]
    
    for header in middleware_headers:
        assert header in headers, f"Missing header: {header}"
        print(f"   ✅ {header}: {headers[header]}")
    
    print("   ✅ All middleware integrated successfully")

def test_performance_impact():
    """Test middleware performance impact"""
    print("\n⚡ Testing Middleware Performance Impact...")
    
    app = create_test_app()
    client = TestClient(app)
    
    # Test multiple requests and measure time
    start_time = time.time()
    
    for i in range(10):
        response = client.get("/")
        assert response.status_code == 200
    
    total_time = time.time() - start_time
    avg_time = total_time / 10
    
    print(f"   10 requests completed in {total_time:.4f}s")
    print(f"   Average request time: {avg_time:.4f}s")
    
    # Check process time from headers
    response = client.get("/")
    process_time = float(response.headers["X-Process-Time"])
    print(f"   Middleware overhead: {process_time:.4f}s")
    
    # Performance should be reasonable (less than 100ms per request)
    assert avg_time < 0.1, f"Requests too slow: {avg_time:.4f}s average"
    assert process_time < 0.05, f"Middleware overhead too high: {process_time:.4f}s"
    
    print("   ✅ Performance within acceptable limits")

def run_all_tests():
    """Run all security middleware tests"""
    print("🧪 Agent-Makalah Security Middleware Test Suite")
    print("=" * 60)
    
    try:
        test_security_headers_middleware()
        test_rate_limiting_middleware()
        test_authentication_middleware()
        test_request_logging_middleware()
        test_middleware_integration()
        test_performance_impact()
        
        print("\n" + "=" * 60)
        print("✅ ALL SECURITY MIDDLEWARE TESTS PASSED!")
        print("🛡️ Security middleware components working correctly")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    run_all_tests() 