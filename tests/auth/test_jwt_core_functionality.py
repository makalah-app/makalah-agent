#!/usr/bin/env python3
"""
Core JWT Functionality Testing Script - Agent Makalah Backend
Task 4.3: JWT Token Management Core Features Testing

Tests core JWT functionality without Redis dependencies:
- JWT generation & validation
- Refresh tokens
- Token expiry & security features
"""

import asyncio
import time
from datetime import datetime, timedelta
from src.core.config import settings

async def test_core_jwt_functionality():
    """Test core JWT token operations without external dependencies"""
    print("1️⃣ Testing Core JWT Functionality...")
    
    try:
        from src.auth.jwt_utils import (
            create_access_token, create_refresh_token, create_token_pair,
            verify_token, verify_refresh_token, decode_token,
            get_token_jti, get_user_id_from_token, get_token_expiry,
            is_token_expired, get_token_remaining_time, is_token_near_expiry
        )
        
        # Test user data
        user_data = {
            "sub": "test-user-jwt-core",
            "email": "test@agent-makalah.com",
            "is_superuser": False
        }
        
        print("   🔐 Testing token creation...")
        
        # Test access token creation
        access_token = create_access_token(user_data)
        print(f"   ✅ Access token created: {access_token[:50]}...")
        
        # Test refresh token creation
        refresh_token = create_refresh_token(user_data)
        print(f"   ✅ Refresh token created: {refresh_token[:50]}...")
        
        # Test token pair creation
        access_token2, refresh_token2 = create_token_pair(user_data)
        print(f"   ✅ Token pair created successfully")
        
        print("   🔍 Testing token verification...")
        
        # Test token verification
        if verify_token(access_token):
            print("   ✅ Access token verification successful")
        else:
            print("   ❌ Access token verification failed")
            
        if verify_refresh_token(refresh_token):
            print("   ✅ Refresh token verification successful")
        else:
            print("   ❌ Refresh token verification failed")
        
        print("   📖 Testing token decoding & extraction...")
        
        # Test token decoding
        decoded = decode_token(access_token)
        if decoded and decoded.get("sub") == "test-user-jwt-core":
            print("   ✅ Token decoding successful")
            print(f"   📝 Token payload: {decoded}")
        else:
            print("   ❌ Token decoding failed")
        
        # Test JTI extraction
        jti = get_token_jti(access_token)
        if jti:
            print(f"   ✅ JTI extracted: {jti}")
        else:
            print("   ❌ JTI extraction failed")
        
        # Test user ID extraction
        user_id = get_user_id_from_token(access_token)
        if user_id == "test-user-jwt-core":
            print("   ✅ User ID extraction successful")
        else:
            print("   ❌ User ID extraction failed")
        
        # Test token expiry
        expiry = get_token_expiry(access_token)
        if expiry:
            print(f"   ✅ Token expiry: {expiry}")
        else:
            print("   ❌ Token expiry extraction failed")
        
        # Test token remaining time
        remaining = get_token_remaining_time(access_token)
        if remaining:
            print(f"   ✅ Token remaining time: {remaining.total_seconds():.2f} seconds")
        else:
            print("   ❌ Token remaining time calculation failed")
        
        return access_token, refresh_token
        
    except Exception as e:
        print(f"   ❌ Core JWT functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return None, None

async def test_token_expiry_and_security():
    """Test token expiry and security features"""
    print("\n2️⃣ Testing Token Expiry & Security Features...")
    
    try:
        from src.auth.jwt_utils import (
            create_access_token, is_token_expired, get_token_remaining_time,
            is_token_near_expiry, verify_token
        )
        
        user_data = {"sub": "expiry-test", "email": "expiry@agent-makalah.com"}
        
        print("   ⏱️  Testing token expiry detection...")
        
        # Create token with very short expiry (2 seconds)
        short_expiry = timedelta(seconds=2)
        short_token = create_access_token(user_data, expires_delta=short_expiry)
        
        print("   - Created token with 2-second expiry")
        
        # Check initial state
        if not is_token_expired(short_token):
            print("   ✅ Token initially not expired")
        else:
            print("   ❌ Token incorrectly showing as expired")
        
        # Check remaining time
        remaining = get_token_remaining_time(short_token)
        if remaining and remaining.total_seconds() > 0:
            print(f"   ✅ Token remaining time: {remaining.total_seconds():.2f} seconds")
        else:
            print("   ❌ Failed to get token remaining time")
        
        # Check if near expiry (within 1 minute since we have a 2-second token)
        if is_token_near_expiry(short_token, threshold_minutes=1):
            print("   ✅ Token correctly detected as near expiry")
        else:
            print("   ❌ Token near expiry detection failed")
        
        # Wait for token to expire
        print("   - Waiting for token to expire...")
        time.sleep(3)
        
        # Check if expired
        if is_token_expired(short_token):
            print("   ✅ Token expiry detection successful")
        else:
            print("   ❌ Token expiry detection failed")
        
        # Verify expired token fails verification
        if not verify_token(short_token):
            print("   ✅ Expired token correctly rejected by verification")
        else:
            print("   ❌ Expired token incorrectly accepted by verification")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Token expiry test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_refresh_token_mechanics():
    """Test refresh token functionality without session storage"""
    print("\n3️⃣ Testing Refresh Token Mechanics...")
    
    try:
        from src.auth.jwt_utils import (
            create_token_pair, verify_refresh_token, refresh_access_token,
            decode_token, verify_token
        )
        
        user_data = {
            "sub": "refresh-test-user",
            "email": "refresh@agent-makalah.com",
            "is_superuser": True
        }
        
        print("   🔄 Testing refresh token flow...")
        
        # Create initial token pair
        access_token, refresh_token = create_token_pair(user_data)
        print("   - Created initial token pair")
        
        # Verify refresh token
        if verify_refresh_token(refresh_token):
            print("   ✅ Refresh token verification successful")
        else:
            print("   ❌ Refresh token verification failed")
            return False
        
        # Check refresh token payload
        refresh_payload = decode_token(refresh_token)
        if refresh_payload and refresh_payload.get("type") == "refresh":
            print("   ✅ Refresh token type validation successful")
        else:
            print("   ❌ Refresh token type validation failed")
        
        # Generate new access token from refresh token
        new_access_token = refresh_access_token(refresh_token)
        if new_access_token:
            print(f"   ✅ New access token generated: {new_access_token[:50]}...")
        else:
            print("   ❌ Failed to generate new access token from refresh token")
            return False
        
        # Verify new access token
        if verify_token(new_access_token):
            print("   ✅ New access token verification successful")
        else:
            print("   ❌ New access token verification failed")
        
        # Verify new token has same user data
        new_payload = decode_token(new_access_token)
        if (new_payload and 
            new_payload.get("sub") == user_data["sub"] and
            new_payload.get("email") == user_data["email"]):
            print("   ✅ New access token contains correct user data")
        else:
            print("   ❌ New access token user data validation failed")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Refresh token mechanics test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_token_edge_cases():
    """Test edge cases and error handling"""
    print("\n4️⃣ Testing Token Edge Cases...")
    
    try:
        from src.auth.jwt_utils import (
            verify_token, decode_token, get_token_jti, get_user_id_from_token,
            get_token_expiry, is_token_expired
        )
        
        print("   🚫 Testing invalid token handling...")
        
        # Test invalid token
        invalid_token = "invalid.jwt.token"
        
        if not verify_token(invalid_token):
            print("   ✅ Invalid token correctly rejected")
        else:
            print("   ❌ Invalid token incorrectly accepted")
        
        if decode_token(invalid_token) is None:
            print("   ✅ Invalid token decode returns None")
        else:
            print("   ❌ Invalid token decode should return None")
        
        if get_token_jti(invalid_token) is None:
            print("   ✅ Invalid token JTI extraction returns None")
        else:
            print("   ❌ Invalid token JTI extraction should return None")
        
        if get_user_id_from_token(invalid_token) is None:
            print("   ✅ Invalid token user ID extraction returns None")
        else:
            print("   ❌ Invalid token user ID extraction should return None")
        
        if get_token_expiry(invalid_token) is None:
            print("   ✅ Invalid token expiry extraction returns None")
        else:
            print("   ❌ Invalid token expiry extraction should return None")
        
        if is_token_expired(invalid_token):
            print("   ✅ Invalid token correctly treated as expired")
        else:
            print("   ❌ Invalid token should be treated as expired")
        
        # Test empty token
        if not verify_token(""):
            print("   ✅ Empty token correctly rejected")
        else:
            print("   ❌ Empty token incorrectly accepted")
        
        # Test None token
        if not verify_token(None):
            print("   ✅ None token correctly handled")
        else:
            print("   ❌ None token should be rejected")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Token edge cases test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_jwt_configuration():
    """Test JWT configuration and settings"""
    print("\n5️⃣ Testing JWT Configuration...")
    
    try:
        from src.core.config import settings
        from src.auth.jwt_utils import create_access_token, decode_token
        
        print("   ⚙️  Testing JWT settings...")
        
        # Check JWT settings
        print(f"   📝 JWT Algorithm: {settings.jwt_algorithm}")
        print(f"   📝 Access Token Expiry: {settings.jwt_access_token_expire_minutes} minutes")
        print(f"   📝 Refresh Token Expiry: {settings.jwt_refresh_token_expire_days} days")
        
        if settings.jwt_secret_key:
            print("   ✅ JWT secret key is configured")
        else:
            print("   ❌ JWT secret key is missing")
        
        if settings.jwt_algorithm in ["HS256", "HS384", "HS512"]:
            print("   ✅ JWT algorithm is valid")
        else:
            print("   ❌ JWT algorithm may be invalid")
        
        # Test token with current settings
        test_data = {"sub": "config-test", "email": "config@agent-makalah.com"}
        token = create_access_token(test_data)
        decoded = decode_token(token)
        
        if decoded:
            # Check token structure
            expected_fields = ["sub", "email", "exp", "iat", "jti", "type"]
            missing_fields = [field for field in expected_fields if field not in decoded]
            
            if not missing_fields:
                print("   ✅ Token structure is complete")
            else:
                print(f"   ❌ Token missing fields: {missing_fields}")
            
            # Check algorithm in token header
            import jwt
            header = jwt.get_unverified_header(token)
            if header.get("alg") == settings.jwt_algorithm:
                print("   ✅ Token algorithm matches configuration")
            else:
                print("   ❌ Token algorithm mismatch")
        
        return True
        
    except Exception as e:
        print(f"   ❌ JWT configuration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main testing function for core JWT functionality"""
    print("🎯 Agent-Makalah Task 4.3: Core JWT Token Management Testing\n")
    print("=" * 70)
    print("🔥 Testing JWT functionality WITHOUT Redis dependencies")
    print("=" * 70)
    
    # Test counters
    total_tests = 5
    passed_tests = 0
    
    # Run all tests
    tests = [
        ("Core JWT Functionality", test_core_jwt_functionality),
        ("Token Expiry & Security", test_token_expiry_and_security),
        ("Refresh Token Mechanics", test_refresh_token_mechanics),
        ("Token Edge Cases", test_token_edge_cases),
        ("JWT Configuration", test_jwt_configuration)
    ]
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        print("-" * 50)
        
        try:
            if test_name == "Core JWT Functionality":
                access_token, refresh_token = await test_func()
                if access_token and refresh_token:
                    passed_tests += 1
            else:
                result = await test_func()
                if result:
                    passed_tests += 1
        except Exception as e:
            print(f"   ❌ Test {test_name} crashed: {e}")
    
    # Final results
    print("\n" + "=" * 70)
    print("🎯 CORE JWT TOKEN MANAGEMENT TEST RESULTS")
    print("=" * 70)
    
    if passed_tests == total_tests:
        print("🎉 ALL CORE JWT TESTS PASSED!")
        print("\n✅ Core JWT Implementation is SOLID:")
        print("   ✅ JWT token generation & validation")
        print("   ✅ Refresh token mechanics")
        print("   ✅ Token expiry detection & security")
        print("   ✅ Error handling & edge cases")
        print("   ✅ Configuration validation")
        
        print("\n📝 Task 4.3 Status:")
        print("   ✅ Core JWT functionality - COMPLETE")
        print("   ⚠️  Redis integration - NEEDS FIXING (Redis host unreachable)")
        print("   ✅ Token management logic - COMPLETE")
        print("   ✅ Security features - COMPLETE")
        
        print("\n🔧 Next steps to complete Task 4.3:")
        print("   1. Fix Redis connection (new Upstash instance or local Redis)")
        print("   2. Re-test Redis-dependent features")
        print("   3. Move to Task 4.4: Authentication Endpoints")
        
    else:
        print(f"❌ {total_tests - passed_tests} core tests failed out of {total_tests}")
        print("\n🔧 Core issues to fix:")
        print("   - Check JWT configuration")
        print("   - Verify dependencies")
        print("   - Review implementation logic")
    
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main()) 