"""
Simplified Authentication Endpoints Test
Tests core authentication functionality without Redis dependencies
"""

import sys
import os
import uuid
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from fastapi.testclient import TestClient
from test_app import app

# Test client
client = TestClient(app)

# Generate unique test data
test_id = str(uuid.uuid4())[:8]
TEST_USER_EMAIL = f"test-simple-{test_id}@agent-makalah.com"
TEST_USER_PASSWORD = "TestPassword123!"
TEST_USER_EMAIL_2 = f"test-simple-2-{test_id}@agent-makalah.com"

def test_authentication_flow():
    """Test complete authentication flow"""
    print("🎯 Agent-Makalah Simple Authentication Test")
    print("=" * 50)
    
    # 1. User Registration
    print("\n1️⃣ Testing User Registration...")
    user_data = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    
    response = client.post("/api/v1/auth/register", json=user_data)
    print(f"   Registration status: {response.status_code}")
    
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["user"]["email"] == TEST_USER_EMAIL
    print("   ✅ User registration successful")
    
    # 2. User Login
    print("\n2️⃣ Testing User Login...")
    login_data = {
        "username": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    print(f"   Login status: {response.status_code}")
    
    assert response.status_code == 200
    response_data = response.json()
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    assert response_data["token_type"] == "bearer"
    print("   ✅ User login successful")
    print(f"   📝 Token length: {len(access_token)}")
    
    # 3. Token Verification
    print("\n3️⃣ Testing Token Verification...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = client.get("/api/v1/auth/verify", headers=headers)
    print(f"   Verification status: {response.status_code}")
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["valid"] is True
    print("   ✅ Token verification successful")
    
    # 4. Get Profile
    print("\n4️⃣ Testing Get Profile...")
    response = client.get("/api/v1/auth/profile", headers=headers)
    print(f"   Profile status: {response.status_code}")
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["user"]["email"] == TEST_USER_EMAIL
    print("   ✅ Profile retrieval successful")
    
    # 5. Update Profile
    print("\n5️⃣ Testing Update Profile...")
    update_data = {
        "email": f"updated-{TEST_USER_EMAIL}"
    }
    
    response = client.put("/api/v1/auth/profile", json=update_data, headers=headers)
    print(f"   Update status: {response.status_code}")
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["user"]["email"] == f"updated-{TEST_USER_EMAIL}"
    print("   ✅ Profile update successful")
    
    # 6. Token Refresh
    print("\n6️⃣ Testing Token Refresh...")
    refresh_data = {
        "refresh_token": refresh_token
    }
    
    response = client.post("/api/v1/auth/refresh", json=refresh_data)
    print(f"   Refresh status: {response.status_code}")
    
    assert response.status_code == 200
    response_data = response.json()
    new_access_token = response_data["access_token"]
    assert new_access_token != access_token  # Should be different
    print("   ✅ Token refresh successful")
    print(f"   📝 New token length: {len(new_access_token)}")
    
    # 7. Access with New Token
    print("\n7️⃣ Testing Access with New Token...")
    new_headers = {"Authorization": f"Bearer {new_access_token}"}
    
    response = client.get("/api/v1/auth/profile", headers=new_headers)
    print(f"   New token access status: {response.status_code}")
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["user"]["email"] == f"updated-{TEST_USER_EMAIL}"
    print("   ✅ New token access successful")
    
    # 8. Logout
    print("\n8️⃣ Testing Logout...")
    response = client.post("/api/v1/auth/logout", headers=new_headers)
    print(f"   Logout status: {response.status_code}")
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "success"
    print("   ✅ Logout successful")
    
    # 9. Invalid Credentials
    print("\n9️⃣ Testing Invalid Credentials...")
    login_data = {
        "username": TEST_USER_EMAIL,
        "password": "WrongPassword123!"
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    print(f"   Invalid login status: {response.status_code}")
    
    assert response.status_code == 401
    print("   ✅ Invalid credentials properly rejected")
    
    # 10. Unauthorized Access
    print("\n🔟 Testing Unauthorized Access...")
    response = client.get("/api/v1/auth/profile")
    print(f"   No token status: {response.status_code}")
    
    assert response.status_code == 401
    
    # Invalid token
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/v1/auth/profile", headers=headers)
    print(f"   Invalid token status: {response.status_code}")
    
    assert response.status_code == 401
    print("   ✅ Unauthorized access properly handled")
    
    print("\n" + "=" * 50)
    print("🎉 ALL AUTHENTICATION TESTS PASSED!")
    print("✅ Basic authentication functionality working")
    print("📝 JWT tokens generated and validated correctly")
    print("🔐 User registration, login, logout working")
    print("👤 Profile management working")
    print("🔄 Token refresh working")
    print("🚫 Security properly enforced")
    print("=" * 50)

if __name__ == "__main__":
    test_authentication_flow() 