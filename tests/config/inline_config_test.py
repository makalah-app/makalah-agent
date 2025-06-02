#!/usr/bin/env python3

# Force reload environment
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Read .env file manually to ensure fresh load
def load_env_manually():
    env_values = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_values[key.strip()] = value.strip()
    except FileNotFoundError:
        print("❌ .env file not found!")
        return {}
    return env_values

def main():
    print("🔍 Manual Environment Configuration Test")
    print("=" * 50)
    
    # Load .env manually
    env_vals = load_env_manually()
    
    if not env_vals:
        print("❌ Failed to load .env file!")
        return
    
    # Test key configurations
    anon_key = env_vals.get('SUPABASE_ANON_KEY', '')
    service_key = env_vals.get('SUPABASE_SERVICE_ROLE_KEY', '')
    jwt_secret = env_vals.get('JWT_SECRET_KEY', '')
    redis_url = env_vals.get('UPSTASH_REDIS_URL', '')
    
    print("🔍 Critical Configuration Check:")
    print(f"  Anon Key Length: {len(anon_key)}")
    print(f"  Service Key Length: {len(service_key)}")
    print(f"  Keys Are Different: {'✅ YES' if anon_key != service_key else '❌ NO - SAME!'}")
    
    if anon_key and service_key:
        print(f"  Anon Key End: ...{anon_key[-20:]}")
        print(f"  Service Key End: ...{service_key[-20:]}")
    
    print(f"  JWT Secret Custom: {'✅ YES' if jwt_secret and jwt_secret != 'default-jwt-secret-key-change-in-production' else '❌ NO'}")
    print(f"  Redis URL Set: {'✅ YES' if redis_url else '❌ NO'}")
    
    # Test if pydantic can load this
    try:
        # Temporarily set environment variables
        for key, value in env_vals.items():
            os.environ[key] = value
        
        # Now try to load settings
        from src.core.config import Settings
        settings = Settings()
        
        print(f"\n✅ Pydantic Settings Loaded Successfully!")
        print(f"  Supabase URL: {'✅ SET' if settings.supabase_url else '❌ NOT SET'}")
        print(f"  Service Key Different from Anon: {'✅ YES' if settings.supabase_service_role_key != settings.supabase_anon_key else '❌ NO'}")
        print(f"  JWT Secret Custom: {'✅ YES' if settings.jwt_secret_key != 'default-jwt-secret-key-change-in-production' else '❌ NO'}")
        
    except Exception as e:
        print(f"❌ Error loading pydantic settings: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n✨ Manual configuration test complete!")

if __name__ == "__main__":
    main() 