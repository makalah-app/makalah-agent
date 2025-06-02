#!/usr/bin/env python3
"""
Debug JWT Fix - Agent Makalah Backend
Debug the JWT timestamp fix to understand verification failure
"""

import os
import sys
from datetime import datetime, timedelta

# Force reload environment
def force_reload():
    redis_vars = ['UPSTASH_REDIS_URL', 'UPSTASH_REDIS_TOKEN']
    for var in redis_vars:
        if var in os.environ:
            del os.environ[var]
    
    try:
        from dotenv import load_dotenv
        load_dotenv(override=True)
    except ImportError:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
    
    # Clear module cache
    modules = ['src.core.config', 'src.auth.jwt_utils']
    for module in modules:
        if module in sys.modules:
            del sys.modules[module]

def test_jwt_step_by_step():
    """Debug JWT creation and verification step by step"""
    print("🔍 Debugging JWT Token Creation & Verification")
    
    from src.auth.jwt_utils import create_access_token, verify_token, decode_token
    from src.core.config import settings
    
    print(f"📝 JWT Settings:")
    print(f"   Secret Key: {settings.jwt_secret_key[:20]}...")
    print(f"   Algorithm: {settings.jwt_algorithm}")
    print(f"   Access Token Expire Minutes: {settings.jwt_access_token_expire_minutes}")
    
    # Step 1: Create token
    print(f"1️⃣ Creating access token...")
    user_data = {"sub": "debug-user", "email": "debug@test.com"}
    
    try:
        token = create_access_token(user_data)
        print(f"   ✅ Token created: {token[:50]}...")
    except Exception as e:
        print(f"   ❌ Token creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 2: Decode token to see payload
    print(f"2️⃣ Decoding token payload...")
    try:
        payload = decode_token(token)
        if payload:
            print(f"   ✅ Token decoded successfully")
            print(f"   📝 Payload: {payload}")
            
            # Check timestamp values
            if 'exp' in payload:
                exp_timestamp = payload['exp']
                exp_datetime = datetime.fromtimestamp(exp_timestamp)
                print(f"   📅 Expiry timestamp: {exp_timestamp}")
                print(f"   📅 Expiry datetime: {exp_datetime}")
                print(f"   🕐 Current time: {datetime.utcnow()}")
                
                # Check if token is in future
                if exp_datetime > datetime.utcnow():
                    print(f"   ✅ Token expires in future (valid)")
                else:
                    print(f"   ❌ Token already expired!")
        else:
            print(f"   ❌ Token decoding failed")
            return False
    except Exception as e:
        print(f"   ❌ Token decoding error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 3: Verify token
    print(f"3️⃣ Verifying token...")
    try:
        is_valid = verify_token(token)
        if is_valid:
            print(f"   ✅ Token verification successful")
        else:
            print(f"   ❌ Token verification failed")
            
            # Try manual verification to see what's wrong
            print(f"   🔍 Manual verification attempt...")
            from jose import jwt, JWTError
            
            try:
                manual_payload = jwt.decode(
                    token,
                    settings.jwt_secret_key,
                    algorithms=[settings.jwt_algorithm]
                )
                print(f"   ✅ Manual verification successful: {manual_payload}")
            except JWTError as jwt_err:
                print(f"   ❌ Manual verification failed: {jwt_err}")
                
            return False
    except Exception as e:
        print(f"   ❌ Token verification error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 4: Test short expiry token
    print(f"4️⃣ Testing short expiry token...")
    try:
        short_token = create_access_token(user_data, expires_delta=timedelta(seconds=5))
        short_payload = decode_token(short_token)
        
        if short_payload:
            exp_timestamp = short_payload['exp']
            exp_datetime = datetime.fromtimestamp(exp_timestamp)
            now = datetime.utcnow()
            remaining = (exp_datetime - now).total_seconds()
            
            print(f"   ✅ Short token created")
            print(f"   📅 Expires: {exp_datetime}")
            print(f"   🕐 Current: {now}")
            print(f"   ⏱️  Remaining: {remaining:.2f} seconds")
            
            if 4 <= remaining <= 6:  # Should be ~5 seconds
                print(f"   ✅ Short expiry working correctly!")
                return True
            else:
                print(f"   ❌ Short expiry not working - expected ~5 seconds, got {remaining:.2f}")
                return False
        else:
            print(f"   ❌ Short token decoding failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Short token test error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🎯 JWT Fix Debug Session")
    print("=" * 50)
    
    force_reload()
    success = test_jwt_step_by_step()
    
    print("=" * 50)
    if success:
        print("🎉 JWT system working correctly!")
    else:
        print("❌ JWT system has issues - need more fixes") 