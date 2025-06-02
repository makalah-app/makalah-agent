#!/usr/bin/env python3
"""
Script untuk create table users via Supabase client - Agent Makalah Backend
Authentication user management
"""
from supabase import create_client, Client
from src.core.config import settings

def create_users_table():
    """Create users table via Supabase client"""
    print("🚀 Creating users table via Supabase...")
    
    try:
        # Initialize Supabase client dengan service role key (admin privileges)
        supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key  # Use service role for admin operations
        )
        
        # Create users table via SQL
        sql_create_table = """
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
        """
        
        # Execute SQL via Supabase RPC
        response = supabase.rpc('exec_sql', {'sql': sql_create_table}).execute()
        
        print("✅ Users table created successfully!")
        print(f"   - Response: {response}")
        
        # Insert sample admin user (optional for testing)
        sample_users = [
            {
                "email": "admin@agent-makalah.com",
                "hashed_password": "$2b$12$dummy.hashed.password.for.testing",  # This should be properly hashed
                "is_superuser": True
            }
        ]
        
        # Note: In real implementation, we should use the CRUD functions to create users
        # This is just for initial setup
        insert_response = supabase.table("users").insert(sample_users).execute()
        print("✅ Sample admin user inserted!")
        print(f"   - Inserted {len(insert_response.data)} users")
        print("   - Note: Change the default admin password in production!")
        
        return True
        
    except Exception as e:
        print("❌ Failed to create users table")
        print(f"   - Error: {str(e)}")
        return False

def test_users_table():
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

def check_user_table_schema():
    """Check users table schema"""
    print("\n📋 Checking users table schema...")
    
    try:
        supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key
        )
        
        # Query table schema
        schema_sql = """
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = 'users' 
        AND table_schema = 'public'
        ORDER BY ordinal_position;
        """
        
        response = supabase.rpc('exec_sql', {'sql': schema_sql}).execute()
        
        print("✅ Users table schema:")
        if response.data:
            for column in response.data:
                nullable = "NULL" if column['is_nullable'] == 'YES' else "NOT NULL"
                default = f" DEFAULT {column['column_default']}" if column['column_default'] else ""
                print(f"   - {column['column_name']}: {column['data_type']} {nullable}{default}")
        
        return True
        
    except Exception as e:
        print("❌ Failed to check users table schema")
        print(f"   - Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎯 Agent-Makalah Users Database Setup\n")
    
    # Step 1: Create table
    table_created = create_users_table()
    
    # Step 2: Test table access
    if table_created:
        test_users_table()
        check_user_table_schema()
    
    print("\n" + "="*50)
    print("🔐 Users table setup complete!")
    print("📝 Next steps:")
    print("   1. Test user registration via API")
    print("   2. Test user authentication via API") 
    print("   3. Change default admin password")
    print("="*50) 