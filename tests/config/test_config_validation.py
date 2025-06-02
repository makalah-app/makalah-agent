#!/usr/bin/env python3
"""
Quick validation script to test configuration loading
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.config import settings
from src.auth.session_manager import SessionManager
from src.database.supabase_client import SupabaseClient

def test_configuration():
    """Test if all configurations are loaded correctly"""
    print("🔍 Testing Agent-Makalah Configuration...")
    print("=" * 50)
    
    # Test JWT Configuration
    print("📋 JWT Configuration:")
    print(f"  JWT Secret Key: {'✅ SET' if settings.jwt_secret_key != 'default-jwt-secret-key-change-in-production' else '❌ DEFAULT'}")
    print(f"  JWT Algorithm: {settings.jwt_algorithm}")
    print(f"  Access Token Expiry: {settings.jwt_access_token_expire_minutes} minutes")
    print(f"  Refresh Token Expiry: {settings.jwt_refresh_token_expire_days} days")
    
    # Test Password Configuration
    print("\n🔐 Password Configuration:")
    print(f"  Hash Algorithm: {settings.password_hash_algorithm}")
    print(f"  Hash Rounds: {settings.password_hash_rounds}")
    print(f"  Salt: {'✅ SET' if settings.password_salt != 'default-salt-change-in-production' else '❌ DEFAULT'}")
    
    # Test Supabase Configuration
    print("\n🗄️ Supabase Configuration:")
    print(f"  URL: {'✅ SET' if settings.supabase_url else '❌ NOT SET'}")
    print(f"  Anon Key: {'✅ SET' if settings.supabase_anon_key else '❌ NOT SET'}")
    print(f"  Service Key: {'✅ SET' if settings.supabase_service_role_key else '❌ NOT SET'}")
    print(f"  Database URL: {'✅ SET' if settings.database_url else '❌ NOT SET'}")
    
    # Test Upstash Redis Configuration
    print("\n🔴 Upstash Redis Configuration:")
    print(f"  URL: {'✅ SET' if settings.upstash_redis_url else '❌ NOT SET'}")
    print(f"  Token: {'✅ SET' if settings.upstash_redis_token else '❌ NOT SET'}")
    print(f"  Password: {'✅ SET' if settings.upstash_redis_password else '❌ NOT SET'}")
    
    # Test Session Configuration
    print("\n🍪 Session Configuration:")
    print(f"  Secret Key: {'✅ SET' if settings.session_secret_key != 'default-session-secret-change-in-production' else '❌ DEFAULT'}")
    print(f"  Max Age: {settings.session_max_age} seconds")
    print(f"  Cookie Name: {settings.session_cookie_name}")
    
    print("\n" + "=" * 50)
    
    # Test actual connections
    print("🔗 Testing Actual Connections...")
    
    # Test Supabase connection
    try:
        supabase_client = SupabaseClient()
        health = supabase_client.health_check()
        print(f"  Supabase: {'✅ CONNECTED' if health['database'] == 'connected' else '❌ FAILED'}")
    except Exception as e:
        print(f"  Supabase: ❌ ERROR - {e}")
    
    # Test Redis connection
    try:
        session_manager = SessionManager()
        if session_manager.redis:
            # Test basic Redis operation
            test_key = "test:config_validation"
            session_manager.redis.set(test_key, "test_value")
            result = session_manager.redis.get(test_key)
            session_manager.redis.delete(test_key)
            print(f"  Upstash Redis: {'✅ CONNECTED' if result == 'test_value' else '❌ FAILED'}")
        else:
            print("  Upstash Redis: ❌ NO CONNECTION")
    except Exception as e:
        print(f"  Upstash Redis: ❌ ERROR - {e}")
    
    print("\n✨ Configuration validation complete!")

if __name__ == "__main__":
    test_configuration() 