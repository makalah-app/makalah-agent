"""
Test Authentication API Endpoints for Agent-Makalah Backend
Comprehensive testing of registration, login, logout, profile, and token refresh
"""

import pytest
import asyncio
import sys
import os
from datetime import datetime
from typing import Dict, Any
import json

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from fastapi.testclient import TestClient
from test_app import app
from src.models.user import UserCreate, UserUpdate
from src.crud.crud_user import UserCRUD
from src.auth.jwt_utils import verify_token, get_user_id_from_token
from src.auth.token_blacklist import TokenBlacklist
from src.auth.enhanced_session_manager import EnhancedSessionManager

# Test client
client = TestClient(app)

# Test data
TEST_USER_EMAIL = "test-auth-endpoints@agent-makalah.com"
TEST_USER_PASSWORD = "TestPassword123!"
TEST_USER_EMAIL_2 = "test-auth-endpoints-2@agent-makalah.com"


class TestAuthenticationEndpoints:
    """Test class for authentication endpoints"""
    
    @classmethod
    def setup_class(cls):
        """Setup test class"""
        cls.user_crud = UserCRUD()
        cls.token_blacklist = TokenBlacklist()
        cls.session_manager = EnhancedSessionManager()
        cls.access_token = None
        cls.refresh_token = None
        cls.user_id = None
    
    def test_01_user_registration(self):
        """Test user registration endpoint"""
        print("\n🧪 1️⃣ Testing User Registration...")
        
        # Test successful registration
        user_data = {
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        print(f"   📝 Registration response status: {response.status_code}")
        print(f"   📝 Registration response: {response.json()}")
        
        assert response.status_code == 201
        
        response_data = response.json()
        assert "user" in response_data
        assert "message" in response_data
        assert response_data["user"]["email"] == TEST_USER_EMAIL
        assert response_data["user"]["is_active"] is True
        assert response_data["message"] == "User registered successfully"
        
        # Store user ID for later tests
        self.__class__.user_id = response_data["user"]["id"]
        
        print("   ✅ User registration successful")
    
    def test_02_duplicate_user_registration(self):
        """Test registration with existing email"""
        print("\n🧪 2️⃣ Testing Duplicate User Registration...")
        
        user_data = {
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        print(f"   📝 Duplicate registration status: {response.status_code}")
        
        assert response.status_code == 400
        
        response_data = response.json()
        assert "already exists" in response_data["detail"]
        
        print("   ✅ Duplicate registration properly rejected")
    
    def test_03_user_login(self):
        """Test user login endpoint"""
        print("\n🧪 3️⃣ Testing User Login...")
        
        # Test successful login
        login_data = {
            "username": TEST_USER_EMAIL,  # OAuth2PasswordRequestForm uses username field
            "password": TEST_USER_PASSWORD
        }
        
        response = client.post("/api/v1/auth/login", data=login_data)
        print(f"   📝 Login response status: {response.status_code}")
        print(f"   📝 Login response keys: {list(response.json().keys())}")
        
        assert response.status_code == 200
        
        response_data = response.json()
        required_fields = ["access_token", "refresh_token", "token_type", "expires_in", "session_id", "user", "message"]
        
        for field in required_fields:
            assert field in response_data, f"Missing field: {field}"
        
        assert response_data["token_type"] == "bearer"
        assert response_data["message"] == "Login successful"
        assert response_data["user"]["email"] == TEST_USER_EMAIL
        
        # Store tokens for subsequent tests
        self.__class__.access_token = response_data["access_token"]
        self.__class__.refresh_token = response_data["refresh_token"]
        
        # Verify token is valid
        assert verify_token(self.access_token)
        
        print("   ✅ User login successful")
        print(f"   📝 Access token length: {len(self.access_token)}")
        print(f"   📝 Session ID: {response_data['session_id']}")
    
    def test_04_invalid_login(self):
        """Test login with invalid credentials"""
        print("\n🧪 4️⃣ Testing Invalid Login...")
        
        # Test with wrong password
        login_data = {
            "username": TEST_USER_EMAIL,
            "password": "WrongPassword123!"
        }
        
        response = client.post("/api/v1/auth/login", data=login_data)
        print(f"   📝 Invalid login status: {response.status_code}")
        
        assert response.status_code == 401
        
        response_data = response.json()
        assert "Incorrect email or password" in response_data["detail"]
        
        print("   ✅ Invalid login properly rejected")
    
    def test_05_token_verification(self):
        """Test token verification endpoint"""
        print("\n🧪 5️⃣ Testing Token Verification...")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        response = client.get("/api/v1/auth/verify", headers=headers)
        print(f"   📝 Token verification status: {response.status_code}")
        
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["valid"] is True
        assert "user" in response_data
        assert response_data["user"]["email"] == TEST_USER_EMAIL
        
        print("   ✅ Token verification successful")
    
    def test_06_get_user_profile(self):
        """Test get user profile endpoint"""
        print("\n🧪 6️⃣ Testing Get User Profile...")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        response = client.get("/api/v1/auth/profile", headers=headers)
        print(f"   📝 Profile get status: {response.status_code}")
        
        assert response.status_code == 200
        
        response_data = response.json()
        assert "user" in response_data
        assert "session_info" in response_data
        assert response_data["user"]["email"] == TEST_USER_EMAIL
        assert response_data["message"] == "Profile retrieved successfully"
        
        print("   ✅ Profile retrieval successful")
        print(f"   📝 Active sessions: {response_data['session_info']['active_sessions']}")
    
    def test_07_update_user_profile(self):
        """Test update user profile endpoint"""
        print("\n🧪 7️⃣ Testing Update User Profile...")
        
        # Register a second user to test email uniqueness
        user_data_2 = {
            "email": TEST_USER_EMAIL_2,
            "password": TEST_USER_PASSWORD
        }
        
        response = client.post("/api/v1/auth/register", json=user_data_2)
        assert response.status_code == 201
        
        # Now test profile update
        headers = {"Authorization": f"Bearer {self.access_token}"}
        update_data = {
            "email": f"updated-{TEST_USER_EMAIL}"
        }
        
        response = client.put("/api/v1/auth/profile", json=update_data, headers=headers)
        print(f"   📝 Profile update status: {response.status_code}")
        
        assert response.status_code == 200
        
        response_data = response.json()
        assert "user" in response_data
        assert response_data["user"]["email"] == f"updated-{TEST_USER_EMAIL}"
        assert response_data["message"] == "Profile updated successfully"
        
        print("   ✅ Profile update successful")
    
    def test_08_token_refresh(self):
        """Test token refresh endpoint"""
        print("\n🧪 8️⃣ Testing Token Refresh...")
        
        # Test refresh token functionality
        refresh_data = {
            "refresh_token": self.refresh_token
        }
        
        response = client.post("/api/v1/auth/refresh", json=refresh_data)
        print(f"   📝 Token refresh status: {response.status_code}")
        
        assert response.status_code == 200
        
        response_data = response.json()
        assert "access_token" in response_data
        assert "token_type" in response_data
        assert "expires_in" in response_data
        assert response_data["token_type"] == "bearer"
        assert response_data["message"] == "Token refreshed successfully"
        
        # Update stored access token
        new_access_token = response_data["access_token"]
        assert verify_token(new_access_token)
        assert new_access_token != self.access_token  # Should be different
        
        # Update for subsequent tests
        self.__class__.access_token = new_access_token
        
        print("   ✅ Token refresh successful")
        print(f"   📝 New token length: {len(new_access_token)}")
    
    def test_09_access_protected_endpoint(self):
        """Test accessing protected endpoint with new token"""
        print("\n🧪 9️⃣ Testing Protected Endpoint Access...")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        response = client.get("/api/v1/auth/profile", headers=headers)
        print(f"   📝 Protected access status: {response.status_code}")
        
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["user"]["email"] == f"updated-{TEST_USER_EMAIL}"
        
        print("   ✅ Protected endpoint access successful")
    
    def test_10_logout_user(self):
        """Test user logout endpoint"""
        print("\n🧪 🔟 Testing User Logout...")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        response = client.post("/api/v1/auth/logout", headers=headers)
        print(f"   📝 Logout status: {response.status_code}")
        
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["message"] == "Logged out successfully"
        assert response_data["status"] == "success"
        
        print("   ✅ User logout successful")
    
    def test_11_access_after_logout(self):
        """Test accessing protected endpoint after logout"""
        print("\n🧪 1️⃣1️⃣ Testing Access After Logout...")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        response = client.get("/api/v1/auth/profile", headers=headers)
        print(f"   📝 Post-logout access status: {response.status_code}")
        
        # Should be unauthorized because token is blacklisted
        assert response.status_code == 401
        
        response_data = response.json()
        assert "Could not validate credentials" in response_data["detail"]
        
        print("   ✅ Post-logout access properly denied")
    
    def test_12_login_after_logout(self):
        """Test login again after logout"""
        print("\n🧪 1️⃣2️⃣ Testing Login After Logout...")
        
        login_data = {
            "username": f"updated-{TEST_USER_EMAIL}",
            "password": TEST_USER_PASSWORD
        }
        
        response = client.post("/api/v1/auth/login", data=login_data)
        print(f"   📝 Re-login status: {response.status_code}")
        
        assert response.status_code == 200
        
        response_data = response.json()
        assert "access_token" in response_data
        assert response_data["user"]["email"] == f"updated-{TEST_USER_EMAIL}"
        
        # Store new tokens
        self.__class__.access_token = response_data["access_token"]
        self.__class__.refresh_token = response_data["refresh_token"]
        
        print("   ✅ Re-login successful")
    
    def test_13_logout_all_sessions(self):
        """Test logout from all sessions"""
        print("\n🧪 1️⃣3️⃣ Testing Logout All Sessions...")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        response = client.post("/api/v1/auth/logout-all", headers=headers)
        print(f"   📝 Logout all status: {response.status_code}")
        
        assert response.status_code == 200
        
        response_data = response.json()
        assert "Logged out from all sessions" in response_data["message"]
        assert response_data["status"] == "success"
        
        print("   ✅ Logout all sessions successful")
        print(f"   📝 {response_data['message']}")
    
    def test_14_unauthorized_access(self):
        """Test accessing endpoints without token"""
        print("\n🧪 1️⃣4️⃣ Testing Unauthorized Access...")
        
        # Test accessing protected endpoint without token
        response = client.get("/api/v1/auth/profile")
        print(f"   📝 No token access status: {response.status_code}")
        
        assert response.status_code == 401
        
        # Test with invalid token
        headers = {"Authorization": "Bearer invalid_token_here"}
        response = client.get("/api/v1/auth/profile", headers=headers)
        print(f"   📝 Invalid token access status: {response.status_code}")
        
        assert response.status_code == 401
        
        print("   ✅ Unauthorized access properly handled")
    
    async def test_15_cleanup_test_data(self):
        """Clean up test data"""
        print("\n🧪 1️⃣5️⃣ Cleaning Up Test Data...")
        
        try:
            # Clean up test users
            user1 = await self.user_crud.get_user_by_email(f"updated-{TEST_USER_EMAIL}")
            user2 = await self.user_crud.get_user_by_email(TEST_USER_EMAIL_2)
            
            if user1:
                await self.user_crud.delete_user(str(user1.id))
                print(f"   🗑️ Deleted user: {user1.email}")
            
            if user2:
                await self.user_crud.delete_user(str(user2.id))
                print(f"   🗑️ Deleted user: {user2.email}")
            
            print("   ✅ Test data cleanup completed")
            
        except Exception as e:
            print(f"   ⚠️ Cleanup error: {str(e)}")


def run_tests():
    """Run all authentication endpoint tests"""
    print("🎯 Agent-Makalah Authentication Endpoints Test Suite")
    print("=" * 60)
    
    test_class = TestAuthenticationEndpoints()
    test_class.setup_class()
    
    try:
        # Run all test methods in order
        test_methods = [
            test_class.test_01_user_registration,
            test_class.test_02_duplicate_user_registration,
            test_class.test_03_user_login,
            test_class.test_04_invalid_login,
            test_class.test_05_token_verification,
            test_class.test_06_get_user_profile,
            test_class.test_07_update_user_profile,
            test_class.test_08_token_refresh,
            test_class.test_09_access_protected_endpoint,
            test_class.test_10_logout_user,
            test_class.test_11_access_after_logout,
            test_class.test_12_login_after_logout,
            test_class.test_13_logout_all_sessions,
            test_class.test_14_unauthorized_access,
        ]
        
        failed_tests = 0
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                print(f"   ❌ Test failed: {str(e)}")
                failed_tests += 1
        
        # Run async cleanup
        asyncio.run(test_class.test_15_cleanup_test_data())
        
        # Results
        print("\n" + "=" * 60)
        total_tests = len(test_methods)
        passed_tests = total_tests - failed_tests
        
        if failed_tests == 0:
            print("🎉 ALL AUTHENTICATION ENDPOINT TESTS PASSED!")
        else:
            print(f"❌ {failed_tests} out of {total_tests} tests failed")
        
        print(f"✅ {passed_tests}/{total_tests} tests passed")
        print("=" * 60)
        
        return failed_tests == 0
        
    except Exception as e:
        print(f"❌ Test suite error: {str(e)}")
        return False


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1) 