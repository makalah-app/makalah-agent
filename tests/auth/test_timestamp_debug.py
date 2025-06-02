#!/usr/bin/env python3
"""
Timestamp Debug - Agent Makalah Backend
Debug JWT timestamp issues
"""

from datetime import datetime, timedelta
import time

def debug_timestamps():
    """Debug timestamp calculations"""
    print("🕐 Timestamp Debug Analysis\n")
    
    # Current times
    now_utc = datetime.utcnow()
    now_local = datetime.now()
    current_timestamp = time.time()
    
    print(f"📅 Current UTC time: {now_utc}")
    print(f"📅 Current local time: {now_local}")
    print(f"📅 Current timestamp: {current_timestamp}")
    print(f"📅 Timestamp to datetime: {datetime.fromtimestamp(current_timestamp)}")
    print(f"📅 UTC timestamp to datetime: {datetime.utcfromtimestamp(current_timestamp)}")
    
    # Test JWT creation timestamps
    print(f"\n🔧 JWT Token Creation Debug...")
    
    # Calculate expiry like in our JWT code
    expire_minutes = 30
    expire = now_utc + timedelta(minutes=expire_minutes)
    expire_timestamp = int(expire.timestamp())
    iat_timestamp = int(now_utc.timestamp())
    
    print(f"📝 IAT (issued at): {iat_timestamp} -> {datetime.fromtimestamp(iat_timestamp)}")
    print(f"📝 EXP (expires): {expire_timestamp} -> {datetime.fromtimestamp(expire_timestamp)}")
    print(f"📝 Token lifetime: {(expire_timestamp - iat_timestamp) / 60:.2f} minutes")
    
    # Check if token should be valid now
    current_ts = int(time.time())
    print(f"📝 Current timestamp: {current_ts}")
    print(f"📝 Token valid? {current_ts < expire_timestamp}")
    print(f"📝 Time difference: {expire_timestamp - current_ts} seconds")
    
    # Test manual JWT
    print(f"\n🧪 Manual JWT Test...")
    
    try:
        from jose import jwt
        from src.core.config import settings
        
        payload = {
            "sub": "debug-user",
            "email": "debug@test.com",
            "exp": expire_timestamp,
            "iat": iat_timestamp,
            "jti": "test-jti",
            "type": "access"
        }
        
        print(f"📝 Creating JWT with payload: {payload}")
        
        token = jwt.encode(
            payload,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm
        )
        
        print(f"✅ JWT created: {token[:50]}...")
        
        # Try to decode immediately
        try:
            decoded = jwt.decode(
                token,
                settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm]
            )
            print(f"✅ JWT decoded successfully: {decoded}")
            return True
        except Exception as decode_err:
            print(f"❌ JWT decode failed: {decode_err}")
            return False
            
    except Exception as e:
        print(f"❌ Manual JWT test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_timezone_fix():
    """Test with different timezone approaches"""
    print(f"\n🌍 Timezone Fix Test...")
    
    from src.core.config import settings
    from jose import jwt
    import time
    
    # Test different timestamp approaches
    approaches = [
        ("UTC datetime.timestamp()", datetime.utcnow().timestamp()),
        ("Local time.time()", time.time()),
        ("UTC timestamp from time", time.mktime(datetime.utcnow().timetuple())),
    ]
    
    for name, timestamp in approaches:
        print(f"\n📝 Testing {name}: {timestamp}")
        
        expire_ts = int(timestamp + 1800)  # 30 minutes
        iat_ts = int(timestamp)
        
        payload = {
            "sub": "tz-test",
            "exp": expire_ts,
            "iat": iat_ts,
            "type": "access"
        }
        
        try:
            token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
            decoded = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
            print(f"   ✅ {name} - SUCCESS")
        except Exception as e:
            print(f"   ❌ {name} - FAILED: {e}")

if __name__ == "__main__":
    success = debug_timestamps()
    test_timezone_fix()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Timestamps working correctly!")
    else:
        print("❌ Timestamp issues found") 