#!/usr/bin/env python3
"""
Simple JWT Test - Agent Makalah Backend
Fresh simple test without complex module reloading
"""

from datetime import datetime, timedelta
import json

def test_jwt_direct():
    """Test JWT directly with fresh imports"""
    print("🎯 Simple JWT Test\n")
    
    # Fresh import after environment is set
    from src.core.config import settings
    print(f"📝 JWT Secret: {settings.jwt_secret_key[:30]}...")
    print(f"📝 JWT Algorithm: {settings.jwt_algorithm}")
    print(f"📝 JWT Expire Minutes: {settings.jwt_access_token_expire_minutes}")
    
    # Test 1: Basic token creation
    print("\n1️⃣ Creating token...")
    try:
        from src.auth.jwt_utils import create_access_token, decode_token, verify_token
        
        user_data = {"sub": "test-user", "email": "test@example.com"}
        token = create_access_token(user_data)
        
        print(f"   ✅ Token created: {token[:50]}...")
        
        # Test 2: Decode token
        print("\n2️⃣ Decoding token...")
        payload = decode_token(token)
        
        if payload:
            print(f"   ✅ Token decoded successfully")
            print(f"   📝 Payload: {json.dumps(payload, indent=2)}")
        else:
            print(f"   ❌ Token decoding failed")
            
            # Manual decode test
            print("\n   🔍 Manual decode test...")
            from jose import jwt
            try:
                manual_payload = jwt.decode(
                    token,
                    settings.jwt_secret_key,
                    algorithms=[settings.jwt_algorithm]
                )
                print(f"   ✅ Manual decode success: {manual_payload}")
            except Exception as e:
                print(f"   ❌ Manual decode failed: {e}")
            return False
        
        # Test 3: Verify token
        print("\n3️⃣ Verifying token...")
        is_valid = verify_token(token)
        
        if is_valid:
            print(f"   ✅ Token verification successful")
        else:
            print(f"   ❌ Token verification failed")
            return False
        
        # Test 4: Short expiry token
        print("\n4️⃣ Testing short expiry...")
        short_token = create_access_token(user_data, expires_delta=timedelta(seconds=5))
        short_payload = decode_token(short_token)
        
        if short_payload:
            exp_timestamp = short_payload['exp']
            exp_datetime = datetime.fromtimestamp(exp_timestamp)
            now = datetime.utcnow()
            remaining = (exp_datetime - now).total_seconds()
            
            print(f"   ✅ Short token created")
            print(f"   ⏱️  Remaining: {remaining:.2f} seconds")
            
            if 4 <= remaining <= 6:
                print(f"   ✅ Token expiry working correctly!")
                return True
            else:
                print(f"   ❌ Token expiry issue - expected ~5s, got {remaining:.2f}s")
                return False
        else:
            print(f"   ❌ Short token decode failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_jwt_direct()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 JWT SYSTEM WORKING PERFECTLY!")
    else:
        print("❌ JWT system still has issues") 