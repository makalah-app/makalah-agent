#!/usr/bin/env python3
"""
Advanced script to create users table via Supabase - Agent Makalah Backend
Authentication user management - Using multiple approaches
"""
import asyncio
import aiohttp
import json
from supabase import create_client, Client
from src.core.config import settings

async def create_table_via_rest_api():
    """Try to create table via Supabase REST API directly"""
    print("🚀 Attempting to create users table via REST API...")
    
    try:
        # Supabase REST API endpoint for running SQL
        url = f"{settings.supabase_url}/rest/v1/rpc/sql"
        
        headers = {
            "apikey": settings.supabase_service_role_key,
            "Authorization": f"Bearer {settings.supabase_service_role_key}",
            "Content-Type": "application/json"
        }
        
        sql_query = """
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            email VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            is_superuser BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
        CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active);
        """
        
        data = {"query": sql_query}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    print("✅ Users table created via REST API!")
                    print(f"   - Response: {result}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ REST API failed: {response.status} - {error_text}")
                    return False
                    
    except Exception as e:
        print(f"❌ REST API approach failed: {str(e)}")
        return False

def create_table_via_postgrest():
    """Try to create table via PostgREST style"""
    print("🚀 Attempting to create users table via PostgREST...")
    
    try:
        supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key
        )
        
        # Try different RPC functions that might exist
        rpc_functions = [
            'exec', 
            'execute_sql', 
            'run_sql',
            'sql_exec',
            'query'
        ]
        
        sql_create = """
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            email VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            is_superuser BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
        CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active);
        """
        
        for func_name in rpc_functions:
            try:
                print(f"   - Trying RPC function: {func_name}")
                response = supabase.rpc(func_name, {'sql': sql_create}).execute()
                print(f"✅ Success with {func_name}!")
                print(f"   - Response: {response}")
                return True
            except Exception as e:
                print(f"   - {func_name} failed: {str(e)}")
                continue
        
        print("❌ All RPC functions failed")
        return False
        
    except Exception as e:
        print(f"❌ PostgREST approach failed: {str(e)}")
        return False

async def create_table_via_direct_sql():
    """Try to create table via direct SQL connection"""
    print("🚀 Attempting to create users table via direct SQL...")
    
    try:
        import asyncpg
        
        # Extract connection info from Supabase URL
        # Supabase URL format: https://project-ref.supabase.co
        project_ref = settings.supabase_project_ref or settings.supabase_url.split('//')[1].split('.')[0]
        
        # Construct PostgreSQL connection string
        pg_host = f"db.{project_ref}.supabase.co"
        pg_database = "postgres"
        pg_user = "postgres"
        pg_password = settings.postgres_password  # This should be set in config
        pg_port = 5432
        
        if not pg_password:
            print("❌ PostgreSQL password not found in config")
            return False
        
        conn = await asyncpg.connect(
            host=pg_host,
            port=pg_port,
            user=pg_user,
            password=pg_password,
            database=pg_database
        )
        
        sql_create = """
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            email VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            is_superuser BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
        CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active);
        """
        
        await conn.execute(sql_create)
        await conn.close()
        
        print("✅ Users table created via direct SQL connection!")
        return True
        
    except ImportError:
        print("❌ asyncpg not installed. Install with: pip install asyncpg")
        return False
    except Exception as e:
        print(f"❌ Direct SQL approach failed: {str(e)}")
        return False

def create_table_via_admin_api():
    """Try to create table via Supabase Admin API"""
    print("🚀 Attempting to create users table via Admin API...")
    
    try:
        import requests
        
        # Admin API endpoint (if available)
        admin_url = f"{settings.supabase_url}/rest/v1/admin/sql"
        
        headers = {
            "apikey": settings.supabase_service_role_key,
            "Authorization": f"Bearer {settings.supabase_service_role_key}",
            "Content-Type": "application/json"
        }
        
        sql_query = """
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            email VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            is_superuser BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
        CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active);
        """
        
        data = {"sql": sql_query}
        
        response = requests.post(admin_url, headers=headers, json=data)
        
        if response.status_code == 200:
            print("✅ Users table created via Admin API!")
            print(f"   - Response: {response.json()}")
            return True
        else:
            print(f"❌ Admin API failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Admin API approach failed: {str(e)}")
        return False

async def test_crud_functions():
    """Test CRUD functions after table creation"""
    print("\n🧪 Testing CRUD functions...")
    
    try:
        from src.crud.crud_user import user_crud
        from src.models.user import UserCreate
        
        # Test 1: Create a test user
        print("   - Testing user creation...")
        test_user_data = UserCreate(
            email="test@agent-makalah.com",
            password="testpassword123"
        )
        
        created_user = await user_crud.create_user(test_user_data)
        if created_user:
            print(f"   ✅ User created: {created_user.email}")
        else:
            print("   ❌ Failed to create user")
            return False
        
        # Test 2: Get user by email
        print("   - Testing get user by email...")
        found_user = await user_crud.get_user_by_email("test@agent-makalah.com")
        if found_user:
            print(f"   ✅ User found: {found_user.email}")
        else:
            print("   ❌ Failed to find user")
            return False
        
        # Test 3: Authenticate user
        print("   - Testing user authentication...")
        auth_user = await user_crud.authenticate_user("test@agent-makalah.com", "testpassword123")
        if auth_user:
            print(f"   ✅ Authentication successful: {auth_user.email}")
        else:
            print("   ❌ Authentication failed")
            return False
        
        # Test 4: Clean up test user
        print("   - Cleaning up test user...")
        deleted = await user_crud.delete_user(str(found_user.id))
        if deleted:
            print("   ✅ Test user cleaned up")
        else:
            print("   ❌ Failed to clean up test user")
        
        print("\n✅ All CRUD tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ CRUD testing failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main function to try all approaches"""
    print("🎯 Agent-Makalah Advanced Users Table Setup\n")
    
    approaches = [
        ("PostgREST RPC", create_table_via_postgrest),
        ("Admin API", create_table_via_admin_api),
        ("REST API", create_table_via_rest_api),
        ("Direct SQL", create_table_via_direct_sql),
    ]
    
    table_created = False
    
    for name, func in approaches:
        print(f"\n{'='*50}")
        print(f"Trying approach: {name}")
        print('='*50)
        
        try:
            if asyncio.iscoroutinefunction(func):
                result = await func()
            else:
                result = func()
                
            if result:
                table_created = True
                print(f"✅ Success with {name}!")
                break
            else:
                print(f"❌ {name} failed, trying next approach...")
        except Exception as e:
            print(f"❌ {name} crashed: {str(e)}")
            continue
    
    if table_created:
        print(f"\n{'='*50}")
        print("Testing CRUD Functions")
        print('='*50)
        await test_crud_functions()
    else:
        print("\n❌ All approaches failed. Manual table creation required.")
        print("\n📝 Manual SQL for Supabase Dashboard:")
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
        
        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
        CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active);
        """)

if __name__ == "__main__":
    asyncio.run(main()) 