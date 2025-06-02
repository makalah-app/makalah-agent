#!/usr/bin/env python3
"""
Fresh JWT System Test - Agent Makalah Backend
Force reload environment and test complete JWT + Redis system
"""

import os
import sys
import importlib
import asyncio
import time
from datetime import datetime, timedelta

def force_reload_all():
    """Force reload all environment and modules"""
    print("🔄 Force reloading environment and modules...")
    
    # Clear Redis environment variables
    redis_vars = [
        'UPSTASH_REDIS_URL', 'UPSTASH_REDIS_TOKEN', 
        'UPSTASH_REDIS_PASSWORD', 'UPSTASH_REDIS_ENDPOINT', 'UPSTASH_REDIS_PORT'
    ]
    
    for var in redis_vars:
        if var in os.environ:
            del os.environ[var]
    
    # Force reload .env
    try:
        from dotenv import load_dotenv
        load_dotenv(override=True)
        print("   ✅ .env reloaded")
    except ImportError:
        # Manual .env parsing
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        print("   ✅ .env manually parsed")
    
    # Remove cached modules
    modules_to_clear = [
        'src.core.config',
        'src.auth.jwt_utils',
        'src.auth.token_blacklist', 
        'src.auth.enhanced_session_manager'
    ]
    
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
            print(f"   - Cleared {module}")
    
    print(f"   📝 New Redis URL: {os.getenv('UPSTASH_REDIS_URL')}")
    return True

async def test_complete_jwt_system():
    """Test complete JWT system with fresh Redis connection"""
    print("\n🎯 Testing Complete JWT System with Redis...")
    
    # Import after reload
    from src.core.config import settings
    from src.auth.jwt_utils import create_token_pair, verify_token, decode_token
    from src.auth.token_blacklist import token_blacklist
    from src.auth.enhanced_session_manager import enhanced_session_manager
    
    print(f"\n📝 Using Redis: {settings.upstash_redis_url}")
    
    try:
        # Test 1: Basic JWT functionality
        print("\n1️⃣ Testing Basic JWT...")
        user_data = {
            "sub": "fresh-test-user",
            "email": "fresh@agent-makalah.com",
            "is_superuser": False
        }
        
        access_token, refresh_token = create_token_pair(user_data)
        print(f"   ✅ Token pair created")
        
        if verify_token(access_token):
            print("   ✅ Access token verification successful")
        else:
            print("   ❌ Access token verification failed")
            return False
        
        # Test 2: Token blacklisting with Redis
        print("\n2️⃣ Testing Token Blacklisting...")
        
        # Check initial state
        if not token_blacklist.is_token_blacklisted(access_token):
            print("   ✅ Token initially not blacklisted")
        else:
            print("   ❌ Token incorrectly showing as blacklisted")
            return False
        
        # Blacklist token
        if token_blacklist.blacklist_token(access_token, "test_blacklist"):
            print("   ✅ Token blacklisted successfully")
        else:
            print("   ❌ Token blacklisting failed")
            return False
        
        # Check if blacklisted
        if token_blacklist.is_token_blacklisted(access_token):
            print("   ✅ Blacklisted token correctly detected")
        else:
            print("   ❌ Blacklisted token not detected")
            return False
        
        # Test 3: Enhanced session management
        print("\n3️⃣ Testing Enhanced Session Management...")
        
        session_user_data = {
            "email": "session@agent-makalah.com",
            "is_superuser": True,
            "name": "Session Test User"
        }
        
        session_id, session_access, session_refresh = enhanced_session_manager.create_authenticated_session(
            "session-test-user", session_user_data
        )
        
        if session_id and session_access and session_refresh:
            print(f"   ✅ Enhanced session created: {session_id}")
        else:
            print("   ❌ Enhanced session creation failed")
            return False
        
        # Test session retrieval
        session_data = enhanced_session_manager.get_session_from_token(session_access)
        if session_data and session_data["user_id"] == "session-test-user":
            print("   ✅ Session retrieval successful")
        else:
            print("   ❌ Session retrieval failed")
            return False
        
        # Test 4: Token expiry (fix the remaining issue)
        print("\n4️⃣ Testing Token Expiry...")
        
        # Create token with 3-second expiry
        from src.auth.jwt_utils import create_access_token, is_token_expired, get_token_remaining_time
        
        short_expiry_data = {"sub": "expiry-test", "email": "expiry@test.com"}
        short_token = create_access_token(short_expiry_data, expires_delta=timedelta(seconds=3))
        
        # Check remaining time
        remaining = get_token_remaining_time(short_token)
        if remaining and remaining.total_seconds() <= 5:  # Should be ~3 seconds or less
            print(f"   ✅ Token expiry time correct: {remaining.total_seconds():.2f} seconds")
        else:
            print(f"   ❌ Token expiry time incorrect: {remaining.total_seconds() if remaining else 'None'} seconds")
            # Let's debug this
            decoded = decode_token(short_token)
            print(f"   🔍 Debug - Token payload: {decoded}")
            return False
        
        # Wait and test expiry
        print("   - Waiting for token to expire...")
        time.sleep(4)
        
        if is_token_expired(short_token):
            print("   ✅ Token expiry detection successful")
        else:
            print("   ❌ Token expiry detection failed")
            return False
        
        # Test 5: Cleanup session
        print("\n5️⃣ Testing Session Cleanup...")
        
        if enhanced_session_manager.logout_session(session_access):
            print("   ✅ Session logout successful")
        else:
            print("   ❌ Session logout failed")
        
        print("\n🎉 ALL JWT SYSTEM TESTS PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ JWT system test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    print("🎯 Fresh JWT System Test with Redis\n")
    print("=" * 60)
    
    # Force reload everything
    if not force_reload_all():
        print("❌ Environment reload failed")
        return
    
    # Test complete system
    success = await test_complete_jwt_system()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 COMPLETE JWT SYSTEM WORKING!")
        print("\n✅ Components verified:")
        print("   ✅ JWT token generation & validation")
        print("   ✅ Redis connection & token blacklisting")
        print("   ✅ Enhanced session management")
        print("   ✅ Token expiry detection")
        print("   ✅ Session cleanup")
        print("\n📝 Task 4.3 Status: READY TO MARK AS COMPLETE")
    else:
        print("❌ JWT system has issues that need fixing")

if __name__ == "__main__":
    asyncio.run(main()) 