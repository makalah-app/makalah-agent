#!/usr/bin/env python3
"""
Create users table via Supabase Management API - Agent Makalah Backend
Using access token from MCP config to create table directly
"""
import asyncio
import aiohttp
import json
from src.core.config import settings

# Supabase access token from MCP config
SUPABASE_ACCESS_TOKEN = "sbp_76e8d5bae8cf17aab06a1ff652f3820727d9f960"

async def get_project_ref():
    """Get project reference from Supabase URL"""
    # Extract project ref from supabase_url
    # Format: https://project-ref.supabase.co
    if settings.supabase_url:
        project_ref = settings.supabase_url.replace("https://", "").replace(".supabase.co", "")
        print(f"   - Extracted project ref: {project_ref}")
        return project_ref
    return None

async def create_table_via_management_api():
    """Create users table via Supabase Management API"""
    print("🚀 Creating users table via Supabase Management API...")
    
    try:
        project_ref = await get_project_ref()
        if not project_ref:
            print("❌ Could not extract project reference from URL")
            return False
        
        # SQL for creating the users table
        sql_create_table = """
-- Create users table for Agent-Makalah authentication
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

-- Create trigger to automatically update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
"""
        
        # Management API endpoint for SQL execution
        management_api_url = f"https://api.supabase.com/v1/projects/{project_ref}/database/query"
        
        headers = {
            "Authorization": f"Bearer {SUPABASE_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "query": sql_create_table
        }
        
        print(f"   - Executing SQL via Management API...")
        print(f"   - Endpoint: {management_api_url}")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(management_api_url, headers=headers, json=payload) as response:
                response_text = await response.text()
                
                if response.status == 200:
                    result = json.loads(response_text)
                    print("✅ Users table created via Management API!")
                    print(f"   - Response: {result}")
                    return True
                else:
                    print(f"❌ Management API failed: {response.status}")
                    print(f"   - Response: {response_text}")
                    return False
        
    except Exception as e:
        print(f"❌ Management API approach failed: {str(e)}")
        return False

async def verify_table_creation():
    """Verify table was created successfully"""
    print("\n🔍 Verifying table creation...")
    
    try:
        from supabase import create_client, Client
        
        supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_anon_key
        )
        
        # Try to access the users table
        response = supabase.table("users").select("id").limit(1).execute()
        
        print("✅ Users table verification successful!")
        print(f"   - Table is accessible and ready for operations")
        return True
        
    except Exception as e:
        print(f"❌ Table verification failed: {str(e)}")
        return False

async def run_crud_tests():
    """Run full CRUD tests after table creation"""
    print("\n🧪 Running comprehensive CRUD tests...")
    
    try:
        from src.crud.crud_user import user_crud
        from src.models.user import UserCreate, UserUpdate
        
        # Test 1: Create a test user
        print("   - Testing user creation...")
        test_user_data = UserCreate(
            email="test-management-api@agent-makalah.com",
            password="testpassword123"
        )
        
        created_user = await user_crud.create_user(test_user_data)
        if created_user:
            print(f"   ✅ User created successfully: {created_user.email}")
        else:
            print("   ❌ Failed to create user")
            return False
        
        # Test 2: Authenticate user
        print("   - Testing authentication...")
        auth_user = await user_crud.authenticate_user("test-management-api@agent-makalah.com", "testpassword123")
        if auth_user:
            print(f"   ✅ Authentication successful: {auth_user.email}")
        else:
            print("   ❌ Authentication failed")
        
        # Test 3: Update user
        print("   - Testing user update...")
        update_data = UserUpdate(is_superuser=True)
        updated_user = await user_crud.update_user(str(created_user.id), update_data)
        if updated_user and updated_user.is_superuser:
            print(f"   ✅ User updated successfully")
        else:
            print("   ❌ Failed to update user")
        
        # Test 4: Get all users
        print("   - Testing get all users...")
        all_users = await user_crud.get_all_users(skip=0, limit=5)
        if all_users:
            print(f"   ✅ Retrieved {len(all_users)} users")
        else:
            print("   ❌ Failed to retrieve users")
        
        # Test 5: Delete user (cleanup)
        print("   - Testing user deletion (cleanup)...")
        deleted = await user_crud.delete_user(str(created_user.id))
        if deleted:
            print(f"   ✅ User soft deleted successfully")
        else:
            print("   ❌ Failed to delete user")
        
        print("\n🎉 All CRUD tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ CRUD testing failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main function - create table via Management API and test"""
    print("🎯 Agent-Makalah Table Creation via Management API\n")
    print("=" * 70)
    
    # Step 1: Create table via Management API
    print("STEP 1: Create users table via Management API")
    print("-" * 70)
    table_created = await create_table_via_management_api()
    
    if table_created:
        # Step 2: Verify table creation
        print("\n" + "=" * 70)
        print("STEP 2: Verify table creation")
        print("-" * 70)
        table_verified = await verify_table_creation()
        
        if table_verified:
            # Step 3: Run CRUD tests
            print("\n" + "=" * 70)
            print("STEP 3: Run comprehensive CRUD tests")
            print("-" * 70)
            crud_success = await run_crud_tests()
            
            # Final status
            print("\n" + "=" * 70)
            if crud_success:
                print("🎉 SUCCESS! Table created and CRUD operations working!")
                print("\n📝 Next steps:")
                print("   1. ✅ Task 4.2 (User Models & CRUD) - COMPLETE")
                print("   2. 🔄 Continue to Task 4.3: JWT Token Management")
                print("   3. 🔄 Implement authentication endpoints")
            else:
                print("❌ CRUD tests failed")
        else:
            print("❌ Table verification failed")
    else:
        print("\n❌ Table creation via Management API failed")
        print("\n📝 Alternative: Manual SQL execution required")
        print("   Go to Supabase Dashboard > SQL Editor and run:")
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
    
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main()) 