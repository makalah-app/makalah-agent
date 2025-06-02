#!/usr/bin/env python3
"""
Redis Connection Test - Agent Makalah Backend
Test new Upstash Redis credentials
"""

import json
from datetime import datetime
from src.core.config import settings

def test_redis_connection():
    """Test Redis connection with new credentials"""
    print("🔗 Testing Redis Connection...")
    print(f"   Redis URL: {settings.upstash_redis_url}")
    print(f"   Redis Token: {'*' * 20}...")
    
    try:
        from upstash_redis import Redis
        
        # Create Redis connection
        redis = Redis(
            url=settings.upstash_redis_url,
            token=settings.upstash_redis_token
        )
        
        # Test basic operations
        print("\n   🧪 Testing basic Redis operations...")
        
        # Test SET
        test_key = "test:agent_makalah:connection"
        test_value = {
            "message": "Hello from Agent Makalah!",
            "timestamp": datetime.utcnow().isoformat(),
            "test": True
        }
        
        result = redis.set(test_key, json.dumps(test_value))
        if result:
            print("   ✅ Redis SET operation successful")
        else:
            print("   ❌ Redis SET operation failed")
            return False
        
        # Test GET
        retrieved = redis.get(test_key)
        if retrieved:
            data = json.loads(retrieved)
            print("   ✅ Redis GET operation successful")
            print(f"   📝 Retrieved data: {data}")
        else:
            print("   ❌ Redis GET operation failed")
            return False
        
        # Test SETEX (with expiry)
        expire_key = "test:agent_makalah:expire"
        expire_value = {"expires": True}
        expire_result = redis.setex(expire_key, 10, json.dumps(expire_value))  # 10 seconds
        if expire_result:
            print("   ✅ Redis SETEX (with expiry) operation successful")
        else:
            print("   ❌ Redis SETEX operation failed")
        
        # Test key existence
        if redis.exists(test_key):
            print("   ✅ Redis EXISTS operation successful")
        else:
            print("   ❌ Redis EXISTS operation failed")
        
        # Test TTL
        ttl = redis.ttl(expire_key)
        if ttl > 0:
            print(f"   ✅ Redis TTL operation successful: {ttl} seconds remaining")
        else:
            print("   ❌ Redis TTL operation failed")
        
        # Cleanup
        redis.delete(test_key)
        redis.delete(expire_key)
        print("   ✅ Redis cleanup successful")
        
        print("\n🎉 Redis connection test PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ Redis connection test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_token_blacklist_redis():
    """Test token blacklist with new Redis connection"""
    print("\n🔒 Testing Token Blacklist with Redis...")
    
    try:
        from src.auth.token_blacklist import token_blacklist
        from src.auth.jwt_utils import create_access_token
        
        # Create test token
        user_data = {"sub": "redis-test", "email": "redis@agent-makalah.com"}
        test_token = create_access_token(user_data)
        
        print("   - Created test token for blacklist testing")
        
        # Test blacklist operations
        if not token_blacklist.is_token_blacklisted(test_token):
            print("   ✅ Token initially not blacklisted")
        else:
            print("   ❌ Token incorrectly showing as blacklisted")
            return False
        
        # Blacklist the token
        if token_blacklist.blacklist_token(test_token, "redis_test"):
            print("   ✅ Token blacklisted successfully")
        else:
            print("   ❌ Token blacklisting failed")
            return False
        
        # Check if blacklisted
        if token_blacklist.is_token_blacklisted(test_token):
            print("   ✅ Blacklisted token correctly detected")
        else:
            print("   ❌ Blacklisted token not detected")
            return False
        
        # Test user token tracking
        if token_blacklist.track_user_token("redis-test", test_token):
            print("   ✅ User token tracking successful")
        else:
            print("   ❌ User token tracking failed")
        
        print("\n🎉 Token blacklist Redis test PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ Token blacklist Redis test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🎯 Agent-Makalah Redis Connection & Token Blacklist Test\n")
    print("=" * 60)
    
    # Test Redis connection
    redis_success = test_redis_connection()
    
    # Test token blacklist if Redis works
    if redis_success:
        blacklist_success = test_token_blacklist_redis()
        
        if redis_success and blacklist_success:
            print("\n" + "=" * 60)
            print("🎉 ALL REDIS TESTS PASSED!")
            print("✅ Redis connection working")
            print("✅ Token blacklist working")
            print("✅ Ready to test full JWT system")
        else:
            print("\n" + "=" * 60)
            print("❌ Some Redis tests failed")
    else:
        print("\n" + "=" * 60)
        print("❌ Redis connection failed - check credentials") 