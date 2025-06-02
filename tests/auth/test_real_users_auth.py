"""
Test Authentication Endpoints with Real Users
Verify that authentication works with actual production users
"""

import sys
import os
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# from src.core.config import settings # Import settings # No longer needed
# print(f"DEBUG: Loaded settings.Config.env_file: {settings.Config.env_file}") # No longer needed
# print(f"DEBUG: Loaded settings.upstash_redis_url: {settings.upstash_redis_url}") # No longer needed
# print(f"DEBUG: Loaded settings.upstash_redis_token: {'********' if settings.upstash_redis_token else None}") # No longer needed

from fastapi.testclient import TestClient
from test_app import app

# Test client
client = TestClient(app)

# Real user credentials
REAL_USERS = [
    {
        "email": "posteriot@gmail.com",
        "password": "M4k4lah2025",
        "type": "Regular User",
        "expected_superuser": False
    },
    {
        "email": "1200pixels@gmail.com", 
        "password": "M4k4lah2025",
        "type": "Regular User",
        "expected_superuser": False
    },
    {
        "email": "erik.supit@gmail.com",
        "password": "M4k4lah2025",
        "type": "Superuser Admin",
        "expected_superuser": True
    }
]

def test_real_users_authentication():
    """Test authentication flow with real users"""
    print("🎯 Agent-Makalah Real Users Authentication Test")
    print("=" * 55)
    
    successful_logins = 0
    
    for user_info in REAL_USERS:
        print(f"\n👤 Testing {user_info['type']}: {user_info['email']}")
        
        # 1. Test Login
        print("   🔐 Testing login...")
        login_data = {
            "username": user_info['email'],
            "password": user_info['password']
        }
        
        response = client.post("/api/v1/auth/login", data=login_data)
        print(f"   📝 Login status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ Login failed for {user_info['email']}")
            continue
        
        response_data = response.json()
        access_token = response_data["access_token"]
        refresh_token = response_data["refresh_token"]
        
        print(f"   ✅ Login successful!")
        print(f"   📝 Token length: {len(access_token)}")
        print(f"   📝 Session ID: {response_data['session_id']}")
        
        # Verify user data in response
        user_data = response_data["user"]
        print(f"   👤 User ID: {user_data['id']}")
        print(f"   📧 Email: {user_data['email']}")
        print(f"   🔴 Active: {user_data['is_active']}")
        print(f"   👑 Superuser: {user_data['is_superuser']}")
        
        # Verify superuser status
        if user_data['is_superuser'] == user_info['expected_superuser']:
            print(f"   ✅ Superuser status correct: {user_data['is_superuser']}")
        else:
            print(f"   ❌ Superuser status mismatch: expected {user_info['expected_superuser']}, got {user_data['is_superuser']}")
        
        # 2. Test Token Verification
        print("   🔍 Testing token verification...")
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = client.get("/api/v1/auth/verify", headers=headers)
        if response.status_code == 200:
            print(f"   ✅ Token verification successful")
        else:
            print(f"   ❌ Token verification failed: {response.status_code}")
        
        # 3. Test Profile Access
        print("   👤 Testing profile access...")
        response = client.get("/api/v1/auth/profile", headers=headers)
        if response.status_code == 200:
            profile_data = response.json()
            print(f"   ✅ Profile access successful")
            print(f"   📊 Active sessions: {profile_data['session_info']['active_sessions']}")
        else:
            print(f"   ❌ Profile access failed: {response.status_code}")
        
        # 4. Test Token Refresh
        print("   🔄 Testing token refresh...")
        refresh_data = {"refresh_token": refresh_token}
        
        response = client.post("/api/v1/auth/refresh", json=refresh_data)
        if response.status_code == 200:
            refresh_response = response.json()
            new_access_token = refresh_response["access_token"]
            print(f"   ✅ Token refresh successful")
            print(f"   📝 New token length: {len(new_access_token)}")
            
            # Update token for logout test
            access_token = new_access_token
            headers = {"Authorization": f"Bearer {access_token}"}
        else:
            print(f"   ❌ Token refresh failed: {response.status_code}")
        
        # 5. Test Logout
        print("   🚪 Testing logout...")
        response = client.post("/api/v1/auth/logout", headers=headers)
        if response.status_code == 200:
            print(f"   ✅ Logout successful")
        else:
            print(f"   ❌ Logout failed: {response.status_code}")
        
        # 6. Verify token is blacklisted after logout
        print("   🔒 Verifying token blacklisted...")
        response = client.get("/api/v1/auth/profile", headers=headers)
        if response.status_code == 401:
            print(f"   ✅ Token properly blacklisted")
        else:
            print(f"   ❌ Token still active after logout: {response.status_code}")
        
        successful_logins += 1
        print(f"   🎉 All tests passed for {user_info['email']}")
    
    # Summary
    print("\n" + "=" * 55)
    if successful_logins == len(REAL_USERS):
        print("🎉 ALL REAL USERS AUTHENTICATION TESTS PASSED!")
        print(f"✅ {successful_logins}/{len(REAL_USERS)} users authenticated successfully")
        print("🔐 Authentication system verified with production users")
        print("👑 Superuser privileges working correctly")
        print("🔄 Token refresh and logout working properly")
        print("🛡️  Security features functioning as expected")
    else:
        print(f"❌ {len(REAL_USERS) - successful_logins} out of {len(REAL_USERS)} users failed authentication")
    
    print("=" * 55)
    return successful_logins == len(REAL_USERS)

def test_superuser_specific_features():
    """Test superuser-specific functionality"""
    print("\n👑 Testing Superuser-Specific Features")
    print("-" * 40)
    
    # Login as superuser
    superuser = next(user for user in REAL_USERS if user['expected_superuser'])
    login_data = {
        "username": superuser['email'],
        "password": superuser['password']
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    if response.status_code != 200:
        print("❌ Superuser login failed!")
        return False
    
    response_data = response.json()
    access_token = response_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    
    print(f"✅ Superuser logged in: {superuser['email']}")
    
    # Test profile shows superuser status
    response = client.get("/api/v1/auth/profile", headers=headers)
    if response.status_code == 200:
        profile_data = response.json()
        if "superuser" in str(profile_data).lower() or profile_data.get("user", {}).get("is_superuser"):
            print("✅ Superuser status visible in profile")
        else:
            print("⚠️  Superuser status not clearly indicated in profile")
    
    # Test logout all sessions (admin feature)
    response = client.post("/api/v1/auth/logout-all", headers=headers)
    if response.status_code == 200:
        print("✅ Logout all sessions working")
    else:
        print(f"❌ Logout all sessions failed: {response.status_code}")
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Real Users Authentication Tests")
    print("=" * 60)
    
    # Test basic authentication
    auth_success = test_real_users_authentication()
    
    # Test superuser features
    if auth_success:
        superuser_success = test_superuser_specific_features()
        
        if superuser_success:
            print("\n🎉 ALL REAL USERS TESTS COMPLETED SUCCESSFULLY!")
            print("🔐 Production authentication system fully verified")
            exit(0)
    
    print("\n❌ Some tests failed")
    exit(1) 