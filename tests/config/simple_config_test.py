#!/usr/bin/env python3
"""
Simple configuration test without auth imports
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_simple_config():
    """Test basic configuration loading"""
    print("🔍 Testing Basic Configuration Loading...")
    print("=" * 50)
    
    try:
        from src.core.config import settings
        print("✅ Config module loaded successfully!")
        
        # Test key configurations
        print(f"\n📋 Key Settings:")
        print(f"  Environment: {settings.environment}")
        print(f"  Debug: {settings.debug}")
        print(f"  API Host: {settings.api_host}")
        print(f"  API Port: {settings.api_port}")
        
        print(f"\n🗄️ Supabase:")
        print(f"  URL: {'✅ SET' if settings.supabase_url else '❌ NOT SET'}")
        print(f"  Anon Key: {'✅ SET' if settings.supabase_anon_key else '❌ NOT SET'}")
        print(f"  Service Key: {'✅ SET' if settings.supabase_service_role_key else '❌ NOT SET'}")
        
        print(f"\n🔐 JWT:")
        print(f"  Secret: {'✅ CUSTOM' if settings.jwt_secret_key != 'default-jwt-secret-key-change-in-production' else '❌ DEFAULT'}")
        print(f"  Algorithm: {settings.jwt_algorithm}")
        print(f"  Expire Minutes: {settings.jwt_access_token_expire_minutes}")
        
        print(f"\n🔴 Redis:")
        print(f"  Upstash URL: {'✅ SET' if settings.upstash_redis_url else '❌ NOT SET'}")
        print(f"  Upstash Token: {'✅ SET' if settings.upstash_redis_token else '❌ NOT SET'}")
        
        print(f"\n🍪 Session:")
        print(f"  Secret: {'✅ CUSTOM' if settings.session_secret_key != 'default-session-secret-change-in-production' else '❌ DEFAULT'}")
        print(f"  Max Age: {settings.session_max_age}")
        
        # Check if key values look correct
        critical_checks = []
        
        if not settings.supabase_url:
            critical_checks.append("❌ Supabase URL missing")
        elif "pjzzwlethszhjyzxgjmd" not in settings.supabase_url:
            critical_checks.append("❌ Supabase URL doesn't match expected project")
        else:
            critical_checks.append("✅ Supabase URL looks correct")
            
        if not settings.supabase_service_role_key:
            critical_checks.append("❌ Service role key missing")
        elif settings.supabase_service_role_key == settings.supabase_anon_key:
            critical_checks.append("❌ Service role key same as anon key!")
        else:
            critical_checks.append("✅ Service role key is different from anon key")
            
        if settings.jwt_secret_key == "default-jwt-secret-key-change-in-production":
            critical_checks.append("❌ JWT secret is still default")
        else:
            critical_checks.append("✅ JWT secret is customized")
            
        if not settings.upstash_redis_url:
            critical_checks.append("❌ Upstash Redis URL missing")
        elif "optimal-gopher-36442" not in settings.upstash_redis_url:
            critical_checks.append("❌ Upstash URL doesn't match expected")
        else:
            critical_checks.append("✅ Upstash Redis URL looks correct")
        
        print(f"\n🔍 Critical Checks:")
        for check in critical_checks:
            print(f"  {check}")
            
        print("\n✨ Configuration test complete!")
        
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_config() 