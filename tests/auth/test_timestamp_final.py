#!/usr/bin/env python3
"""
Final Timestamp Debug - Agent Makalah Backend
"""

import time
from datetime import datetime, timedelta

def test_short_expiry_debug():
    """Debug short expiry token creation step by step"""
    print("🔍 Short Expiry Token Debug\n")
    
    # Import fresh
    from src.auth.jwt_utils import create_access_token, decode_token, get_token_remaining_time
    
    # Test parameters
    user_data = {"sub": "debug", "email": "debug@test.com"}
    expiry_seconds = 5
    expires_delta = timedelta(seconds=expiry_seconds)
    
    print(f"📝 Creating token with {expiry_seconds} second expiry...")
    print(f"📝 expires_delta: {expires_delta}")
    print(f"📝 expires_delta.total_seconds(): {expires_delta.total_seconds()}")
    
    # Check what's happening in create_access_token
    current_time = int(time.time())
    expire_seconds_calc = int(expires_delta.total_seconds())
    expected_exp = current_time + expire_seconds_calc
    
    print(f"📝 Current time: {current_time}")
    print(f"📝 Expire seconds: {expire_seconds_calc}")
    print(f"📝 Expected exp: {expected_exp}")
    print(f"📝 Expected remaining: {expected_exp - current_time} seconds")
    
    # Create token
    token = create_access_token(user_data, expires_delta=expires_delta)
    print(f"\n✅ Token created")
    
    # Decode and check
    payload = decode_token(token)
    if payload:
        actual_exp = payload["exp"]
        actual_iat = payload["iat"]
        
        print(f"📝 Payload exp: {actual_exp}")
        print(f"📝 Payload iat: {actual_iat}")
        print(f"📝 Token lifetime: {actual_exp - actual_iat} seconds")
        
        # Check remaining time
        remaining = get_token_remaining_time(token)
        if remaining:
            print(f"📝 Remaining time: {remaining.total_seconds():.2f} seconds")
            
            if 4 <= remaining.total_seconds() <= 6:
                print("✅ Short expiry working correctly!")
                return True
            else:
                print(f"❌ Expected ~5 seconds, got {remaining.total_seconds():.2f}")
                
                # Debug the calculation
                current_check = int(time.time())
                manual_remaining = actual_exp - current_check
                print(f"🔍 Manual calculation: {actual_exp} - {current_check} = {manual_remaining}")
                return False
        else:
            print("❌ No remaining time calculated")
            return False
    else:
        print("❌ Token decode failed")
        return False

if __name__ == "__main__":
    success = test_short_expiry_debug()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Short expiry working!")
    else:
        print("❌ Short expiry still broken") 