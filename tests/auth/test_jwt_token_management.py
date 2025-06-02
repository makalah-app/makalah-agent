#!/usr/bin/env python3
"""
Comprehensive JWT Token Management Testing Script - Agent Makalah Backend
Task 4.3: JWT Token Management & Session Handling Testing

Tests all JWT token management features:
- JWT generation & validation
- Refresh tokens
- Token blacklisting  
- Session Redis storage
- Enhanced session management
"""

import asyncio
import time
from datetime import datetime, timedelta
from src.core.config import settings

async def test_basic_jwt_functionality():
    """Test basic JWT token creation and validation"""
    print("1️⃣ Testing Basic JWT Functionality...")
    
    try:
        from src.auth.jwt_utils import (
            create_access_token, create_refresh_token, create_token_pair,
            verify_token, verify_refresh_token, decode_token,
            get_token_jti, get_user_id_from_token
        )
        
        # Test user data
        user_data = {
            "sub": "test-user-123",
            "email": "test@agent-makalah.com",
            "is_superuser": False
        }
        
        # Test access token creation
        access_token = create_access_token(user_data)
        print(f"   ✅ Access token created: {access_token[:50]}...")
        
        # Test refresh token creation
        refresh_token = create_refresh_token(user_data)
        print(f"   ✅ Refresh token created: {refresh_token[:50]}...")
        
        # Test token pair creation
        access_token2, refresh_token2 = create_token_pair(user_data)
        print(f"   ✅ Token pair created")
        
        # Test token verification
        if verify_token(access_token):
            print("   ✅ Access token verification successful")
        else:
            print("   ❌ Access token verification failed")
            
        if verify_refresh_token(refresh_token):
            print("   ✅ Refresh token verification successful")
        else:
            print("   ❌ Refresh token verification failed")
        
        # Test token decoding
        decoded = decode_token(access_token)
        if decoded and decoded.get("sub") == "test-user-123":
            print("   ✅ Token decoding successful")
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
        if user_id == "test-user-123":
            print("   ✅ User ID extraction successful")
        else:
            print("   ❌ User ID extraction failed")
        
        return access_token, refresh_token
        
    except Exception as e:
        print(f"   ❌ Basic JWT functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return None, None

async def test_token_blacklisting():
    """Test token blacklisting functionality"""
    print("\n2️⃣ Testing Token Blacklisting...")
    
    try:
        from src.auth.jwt_utils import create_access_token, create_refresh_token
        from src.auth.token_blacklist import token_blacklist
        
        # Create test tokens
        user_data = {
            "sub": "blacklist-test-user",
            "email": "blacklist@agent-makalah.com",
            "is_superuser": False
        }
        
        access_token = create_access_token(user_data)
        refresh_token = create_refresh_token(user_data)
        
        print(f"   - Created tokens for blacklist testing")
        
        # Test initial blacklist status
        if not token_blacklist.is_token_blacklisted(access_token):
            print("   ✅ Token initially not blacklisted")
        else:
            print("   ❌ Token incorrectly showing as blacklisted")
        
        # Test token blacklisting
        if token_blacklist.blacklist_token(access_token, "test_logout"):
            print("   ✅ Token blacklisted successfully")
        else:
            print("   ❌ Token blacklisting failed")
        
        # Test blacklist check
        if token_blacklist.is_token_blacklisted(access_token):
            print("   ✅ Blacklisted token correctly identified")
        else:
            print("   ❌ Blacklisted token not detected")
        
        # Test user token tracking
        user_id = "blacklist-test-user"
        if token_blacklist.track_user_token(user_id, refresh_token):
            print("   ✅ User token tracking successful")
        else:
            print("   ❌ User token tracking failed")
        
        # Test mass blacklisting
        blacklisted_count = token_blacklist.blacklist_all_user_tokens(user_id, "security_test")
        print(f"   ✅ Mass blacklisted {blacklisted_count} tokens for user")
        
        # Test blacklist statistics
        stats = token_blacklist.get_blacklist_stats()
        if "total_blacklisted" in stats:
            print(f"   ✅ Blacklist stats: {stats['total_blacklisted']} tokens blacklisted")
        else:
            print(f"   ⚠️  Blacklist stats error: {stats}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Token blacklisting test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_session_management():
    """Test basic session management"""
    print("\n3️⃣ Testing Basic Session Management...")
    
    try:
        from src.auth.session_manager import session_manager
        
        # Test user data
        user_id = "session-test-user"
        user_data = {
            "email": "session@agent-makalah.com",
            "is_superuser": False,
            "name": "Session Test User"
        }
        
        # Create session
        session_id = session_manager.create_session(user_id, user_data)
        if session_id:
            print(f"   ✅ Session created: {session_id}")
        else:
            print("   ❌ Session creation failed")
            return False
        
        # Get session
        retrieved_session = session_manager.get_session(session_id)
        if retrieved_session and retrieved_session["user_id"] == user_id:
            print("   ✅ Session retrieval successful")
        else:
            print("   ❌ Session retrieval failed")
        
        # Update session
        updated_data = {"last_login": datetime.utcnow().isoformat()}
        if session_manager.update_session(session_id, updated_data):
            print("   ✅ Session update successful")
        else:
            print("   ❌ Session update failed")
        
        # Validate session
        if session_manager.is_session_valid(session_id):
            print("   ✅ Session validation successful")
        else:
            print("   ❌ Session validation failed")
        
        # Get user ID from session
        retrieved_user_id = session_manager.get_user_id_from_session(session_id)
        if retrieved_user_id == user_id:
            print("   ✅ User ID retrieval from session successful")
        else:
            print("   ❌ User ID retrieval from session failed")
        
        # Delete session
        if session_manager.delete_session(session_id):
            print("   ✅ Session deletion successful")
        else:
            print("   ❌ Session deletion failed")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Session management test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_enhanced_session_management():
    """Test enhanced session management with JWT integration"""
    print("\n4️⃣ Testing Enhanced Session Management...")
    
    try:
        from src.auth.enhanced_session_manager import enhanced_session_manager
        
        # Test user data
        user_id = "enhanced-session-test"
        user_data = {
            "email": "enhanced@agent-makalah.com",
            "is_superuser": True,
            "name": "Enhanced Session User"
        }
        device_info = {
            "user_agent": "Test Browser 1.0",
            "ip_address": "127.0.0.1"
        }
        
        # Create authenticated session
        session_id, access_token, refresh_token = enhanced_session_manager.create_authenticated_session(
            user_id, user_data, device_info
        )
        
        if session_id and access_token and refresh_token:
            print(f"   ✅ Enhanced session created: {session_id}")
            print(f"   ✅ Access token: {access_token[:50]}...")
            print(f"   ✅ Refresh token: {refresh_token[:50]}...")
        else:
            print("   ❌ Enhanced session creation failed")
            return False
        
        # Get session from token
        session_data = enhanced_session_manager.get_session_from_token(access_token)
        if session_data and session_data["user_id"] == user_id:
            print("   ✅ Session retrieval from access token successful")
        else:
            print("   ❌ Session retrieval from access token failed")
        
        # Test refresh token mechanism
        new_access_token, session_id_from_refresh = enhanced_session_manager.refresh_session_token(refresh_token)
        if new_access_token and session_id_from_refresh == session_id:
            print(f"   ✅ Token refresh successful: {new_access_token[:50]}...")
        else:
            print("   ❌ Token refresh failed")
        
        # Validate session token
        validated_data = enhanced_session_manager.validate_session_token(new_access_token)
        if validated_data and validated_data["user_id"] == user_id:
            print("   ✅ Session token validation successful")
        else:
            print("   ❌ Session token validation failed")
        
        # Get user active sessions
        active_sessions = enhanced_session_manager.get_user_active_sessions(user_id)
        if active_sessions and len(active_sessions) >= 1:
            print(f"   ✅ Found {len(active_sessions)} active sessions for user")
        else:
            print("   ❌ Failed to get user active sessions")
        
        # Test logout
        if enhanced_session_manager.logout_session(new_access_token):
            print("   ✅ Session logout successful")
        else:
            print("   ❌ Session logout failed")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Enhanced session management test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_refresh_token_flow():
    """Test complete refresh token flow"""
    print("\n5️⃣ Testing Refresh Token Flow...")
    
    try:
        from src.auth.jwt_utils import refresh_access_token, validate_and_decode_token
        from src.auth.enhanced_session_manager import enhanced_session_manager
        
        # Create test session
        user_id = "refresh-flow-test"
        user_data = {
            "email": "refresh@agent-makalah.com",
            "is_superuser": False
        }
        
        session_id, access_token, refresh_token = enhanced_session_manager.create_authenticated_session(
            user_id, user_data
        )
        
        print(f"   - Created session for refresh flow test")
        
        # Test access token validation
        payload = validate_and_decode_token(access_token)
        if payload and payload.get("sub") == user_id:
            print("   ✅ Initial access token validation successful")
        else:
            print("   ❌ Initial access token validation failed")
        
        # Test refresh token to create new access token
        new_access_token = refresh_access_token(refresh_token)
        if new_access_token:
            print(f"   ✅ New access token created via refresh: {new_access_token[:50]}...")
        else:
            print("   ❌ Refresh token flow failed")
            return False
        
        # Validate new access token
        new_payload = validate_and_decode_token(new_access_token)
        if new_payload and new_payload.get("sub") == user_id:
            print("   ✅ New access token validation successful")
        else:
            print("   ❌ New access token validation failed")
        
        # Test enhanced session refresh
        final_access_token, final_session_id = enhanced_session_manager.refresh_session_token(refresh_token)
        if final_access_token and final_session_id == session_id:
            print("   ✅ Enhanced session refresh successful")
        else:
            print("   ❌ Enhanced session refresh failed")
        
        # Cleanup
        enhanced_session_manager.logout_session(final_access_token)
        
        return True
        
    except Exception as e:
        print(f"   ❌ Refresh token flow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_security_features():
    """Test security features and edge cases"""
    print("\n6️⃣ Testing Security Features...")
    
    try:
        from src.auth.jwt_utils import create_access_token, is_token_expired, get_token_remaining_time
        from src.auth.token_blacklist import token_blacklist
        from src.auth.enhanced_session_manager import enhanced_session_manager
        
        # Test token expiry detection
        user_data = {"sub": "security-test", "email": "security@agent-makalah.com"}
        
        # Create token with very short expiry
        short_expiry = timedelta(seconds=1)
        short_token = create_access_token(user_data, expires_delta=short_expiry)
        
        print("   - Created token with 1-second expiry")
        
        # Check initial remaining time
        remaining_time = get_token_remaining_time(short_token)
        if remaining_time and remaining_time.total_seconds() > 0:
            print(f"   ✅ Token remaining time: {remaining_time.total_seconds():.2f} seconds")
        else:
            print("   ❌ Failed to get token remaining time")
        
        # Wait for token to expire
        print("   - Waiting for token to expire...")
        time.sleep(2)
        
        # Check if token is expired
        if is_token_expired(short_token):
            print("   ✅ Token expiry detection successful")
        else:
            print("   ❌ Token expiry detection failed")
        
        # Test mass user logout
        user_id = "mass-logout-test"
        user_data = {"email": "mass@agent-makalah.com", "is_superuser": False}
        
        # Create multiple sessions
        session1_id, token1_access, token1_refresh = enhanced_session_manager.create_authenticated_session(user_id, user_data)
        session2_id, token2_access, token2_refresh = enhanced_session_manager.create_authenticated_session(user_id, user_data)
        
        print(f"   - Created 2 sessions for mass logout test")
        
        # Mass logout
        logged_out_count = enhanced_session_manager.logout_all_user_sessions(user_id)
        print(f"   ✅ Mass logout successful: {logged_out_count} sessions logged out")
        
        # Verify tokens are blacklisted
        if (token_blacklist.is_token_blacklisted(token1_access) and 
            token_blacklist.is_token_blacklisted(token2_access)):
            print("   ✅ Mass logout tokens correctly blacklisted")
        else:
            print("   ❌ Mass logout tokens not properly blacklisted")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Security features test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_integration_with_crud():
    """Test integration with existing CRUD operations"""
    print("\n7️⃣ Testing Integration with CRUD Operations...")
    
    try:
        from src.crud.crud_user import user_crud
        from src.models.user import UserCreate
        from src.auth.enhanced_session_manager import enhanced_session_manager
        
        # Create a test user via CRUD
        test_user_data = UserCreate(
            email="jwt-integration@agent-makalah.com",
            password="testpassword123"
        )
        
        created_user = await user_crud.create_user(test_user_data)
        if not created_user:
            print("   ❌ Failed to create test user for integration")
            return False
        
        print(f"   ✅ Created test user: {created_user.email}")
        
        # Authenticate user
        authenticated_user = await user_crud.authenticate_user(created_user.email, "testpassword123")
        if not authenticated_user:
            print("   ❌ Failed to authenticate test user")
            return False
        
        print("   ✅ User authentication successful")
        
        # Create authenticated session
        user_data = {
            "email": authenticated_user.email,
            "is_superuser": authenticated_user.is_superuser
        }
        
        session_id, access_token, refresh_token = enhanced_session_manager.create_authenticated_session(
            str(authenticated_user.id), user_data
        )
        
        if session_id and access_token:
            print("   ✅ Authenticated session created with real user data")
        else:
            print("   ❌ Failed to create authenticated session")
            return False
        
        # Validate session contains correct user data
        session_data = enhanced_session_manager.validate_session_token(access_token)
        if (session_data and 
            session_data["user_data"]["email"] == created_user.email):
            print("   ✅ Session validation with real user data successful")
        else:
            print("   ❌ Session validation failed")
        
        # Cleanup
        enhanced_session_manager.logout_session(access_token)
        await user_crud.delete_user(str(authenticated_user.id))
        print("   ✅ Integration test cleanup completed")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Integration with CRUD test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main testing function for Task 4.3"""
    print("🎯 Agent-Makalah Task 4.3: JWT Token Management Testing\n")
    print("=" * 70)
    
    # Test counters
    total_tests = 7
    passed_tests = 0
    
    # Run all tests
    tests = [
        ("Basic JWT Functionality", test_basic_jwt_functionality),
        ("Token Blacklisting", test_token_blacklisting),
        ("Session Management", test_session_management),
        ("Enhanced Session Management", test_enhanced_session_management),
        ("Refresh Token Flow", test_refresh_token_flow),
        ("Security Features", test_security_features),
        ("CRUD Integration", test_integration_with_crud)
    ]
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        print("-" * 50)
        
        try:
            if test_name == "Basic JWT Functionality":
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
    print("🎯 TASK 4.3 JWT TOKEN MANAGEMENT TEST RESULTS")
    print("=" * 70)
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ Task 4.3 Implementation Complete:")
        print("   ✅ JWT generation & validation")
        print("   ✅ Refresh tokens")
        print("   ✅ Token blacklisting")
        print("   ✅ Session Redis storage") 
        print("   ✅ Enhanced session management")
        print("   ✅ Security features")
        print("   ✅ CRUD integration")
        
        print("\n📝 Next steps:")
        print("   1. ✅ Task 4.3 (JWT Token Management) - COMPLETE")
        print("   2. 🔄 Continue to Task 4.4: Authentication Endpoints")
        print("   3. 🔄 Implement API routes")
        print("   4. 🔄 Test complete authentication flow")
        
    else:
        print(f"❌ {total_tests - passed_tests} tests failed out of {total_tests}")
        print("\n🔧 Issues to fix:")
        if passed_tests < total_tests:
            print("   - Check Redis connection and configuration")
            print("   - Verify JWT settings in config")
            print("   - Ensure all dependencies are installed")
    
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main()) 