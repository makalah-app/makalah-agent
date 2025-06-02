#!/usr/bin/env python3
"""
Environment Reload Test - Agent Makalah Backend
Force reload .env and test new Redis credentials
"""

import os
import importlib
import sys

def reload_environment():
    """Force reload environment variables"""
    print("🔄 Reloading environment variables...")
    
    # Clear existing environment variables
    old_redis_vars = [
        'UPSTASH_REDIS_URL',
        'UPSTASH_REDIS_TOKEN', 
        'UPSTASH_REDIS_PASSWORD',
        'UPSTASH_REDIS_ENDPOINT',
        'UPSTASH_REDIS_PORT'
    ]
    
    for var in old_redis_vars:
        if var in os.environ:
            print(f"   - Clearing {var}")
            del os.environ[var]
    
    # Force reload .env file
    try:
        from dotenv import load_dotenv
        load_dotenv(override=True)  # Force reload
        print("   ✅ .env file reloaded")
    except ImportError:
        print("   ⚠️  python-dotenv not available, manual reload...")
        
        # Manual .env parsing
        try:
            with open('.env', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
            print("   ✅ Manual .env parsing complete")
        except Exception as e:
            print(f"   ❌ Failed to read .env: {e}")
            return False
    
    # Check new values
    print(f"\n   📝 New UPSTASH_REDIS_URL: {os.getenv('UPSTASH_REDIS_URL')}")
    print(f"   📝 New UPSTASH_REDIS_TOKEN: {os.getenv('UPSTASH_REDIS_TOKEN', 'NOT_SET')[:20]}...")
    
    return True

def reload_settings():
    """Force reload settings module"""
    print("\n🔄 Reloading settings module...")
    
    # Remove modules from cache
    modules_to_reload = [
        'src.core.config',
        'src.auth.token_blacklist',
        'src.auth.enhanced_session_manager'
    ]
    
    for module_name in modules_to_reload:
        if module_name in sys.modules:
            print(f"   - Reloading {module_name}")
            importlib.reload(sys.modules[module_name])
    
    # Re-import and check
    try:
        from src.core.config import settings
        print(f"\n   📝 Reloaded Redis URL: {settings.upstash_redis_url}")
        print(f"   📝 Reloaded Redis Token: {settings.upstash_redis_token[:20] if settings.upstash_redis_token else 'NOT_SET'}...")
        return settings
    except Exception as e:
        print(f"   ❌ Failed to reload settings: {e}")
        return None

def test_new_redis_connection(settings):
    """Test Redis with reloaded settings"""
    print("\n🔗 Testing Redis with new credentials...")
    
    try:
        from upstash_redis import Redis
        
        redis = Redis(
            url=settings.upstash_redis_url,
            token=settings.upstash_redis_token
        )
        
        # Simple test
        test_key = "test:reload:connection"
        result = redis.set(test_key, "Hello from reloaded Redis!")
        
        if result:
            print("   ✅ Redis connection successful!")
            
            # Get the value back
            value = redis.get(test_key)
            print(f"   📝 Retrieved: {value}")
            
            # Cleanup
            redis.delete(test_key)
            return True
        else:
            print("   ❌ Redis SET failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Redis test failed: {e}")
        return False

if __name__ == "__main__":
    print("🎯 Environment Reload & Redis Test\n")
    print("=" * 50)
    
    # Step 1: Reload environment
    if not reload_environment():
        print("❌ Environment reload failed")
        exit(1)
    
    # Step 2: Reload settings
    settings = reload_settings()
    if not settings:
        print("❌ Settings reload failed")
        exit(1)
    
    # Step 3: Test Redis
    if test_new_redis_connection(settings):
        print("\n🎉 Redis connection working with new credentials!")
    else:
        print("\n❌ Redis connection still failing")
        print("\n🔧 Debug info:")
        print(f"   URL: {settings.upstash_redis_url}")
        print(f"   Token length: {len(settings.upstash_redis_token) if settings.upstash_redis_token else 0}") 