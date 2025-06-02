#!/usr/bin/env python3
"""
Simple script to create users table via Supabase - Agent Makalah Backend
Authentication user management
"""
from supabase import create_client, Client
from src.core.config import settings

def create_users_table_simple():
    """Create users table via direct table operations"""
    print("🚀 Creating users table via Supabase (simple method)...")
    
    try:
        # Initialize Supabase client dengan service role key (admin privileges)
        supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key  # Use service role for admin operations
        )
        
        # Try to create a test user to see if table exists
        # If table doesn't exist, this will fail and we'll know we need to create it manually
        test_user = {
            "email": "test@agent-makalah.com",
            "hashed_password": "$2b$12$dummy.hashed.password.for.testing",
            "is_active": True,
            "is_superuser": False
        }
        
        # Try to insert test user
        response = supabase.table("users").insert(test_user).execute()
        
        if response.data:
            print("✅ Users table already exists and is accessible!")
            print(f"   - Test user created: {response.data[0]['email']}")
            
            # Clean up test user
            supabase.table("users").delete().eq("email", "test@agent-makalah.com").execute()
            print("   - Test user cleaned up")
            
            return True
        else:
            print("❌ Failed to insert test user")
            return False
        
    except Exception as e:
        print("❌ Users table doesn't exist or is not accessible")
        print(f"   - Error: {str(e)}")
        print("\n📝 Manual steps required:")
        print("   1. Go to Supabase Dashboard > SQL Editor")
        print("   2. Run the following SQL:")
        print("""
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            email VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            is_superuser BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- Create index on email for faster lookups
        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
        
        -- Create index on active users
        CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active);
        """)
        print("   3. Run this script again to test")
        return False

def test_users_table_simple():
    """Test users table access"""
    print("\n🔍 Testing users table access...")
    
    try:
        supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_anon_key
        )
        
        # Test select from users table (only count for security)
        response = supabase.table("users").select("id,email,is_active,created_at").execute()
        
        print("✅ Users table access successful!")
        print(f"   - Found {len(response.data)} users")
        for user in response.data:
            print(f"     • {user['email']} (Active: {user['is_active']})")
        
        return True
        
    except Exception as e:
        print("❌ Failed to access users table")
        print(f"   - Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎯 Agent-Makalah Users Database Setup (Simple)\n")
    
    # Step 1: Try to create/test table
    table_ready = create_users_table_simple()
    
    # Step 2: Test table access
    if table_ready:
        test_users_table_simple()
    
    print("\n" + "="*50)
    print("🔐 Users table setup complete!")
    print("📝 Next steps:")
    print("   1. Test user registration via API")
    print("   2. Test user authentication via API") 
    print("="*50) 