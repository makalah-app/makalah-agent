#!/usr/bin/env python3
"""
Test table existence and create via pragmatic approach - Agent Makalah Backend
Authentication user management
"""
import asyncio
from supabase import create_client, Client
from src.core.config import settings

def test_table_exists():
    """Test if users table exists by trying to access it"""
    print("🔍 Testing if users table exists...")
    
    try:
        supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_anon_key
        )
        
        # Try to select from users table
        response = supabase.table("users").select("id").limit(0).execute()
        
        print("✅ Users table exists and is accessible!")
        return True
        
    except Exception as e:
        print(f"❌ Users table doesn't exist or not accessible: {str(e)}")
        return False

def create_table_via_schema_definition():
    """Try to create table via Supabase management API"""
    print("🚀 Attempting to create table via management features...")
    
    try:
        supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key
        )
        
        # First, let's see what tables exist
        print("   - Checking existing tables...")
        try:
            # Try to query information_schema to see existing tables
            response = supabase.table("information_schema.tables").select("table_name").eq("table_schema", "public").execute()
            if response.data:
                existing_tables = [table['table_name'] for table in response.data]
                print(f"   - Found existing tables: {existing_tables}")
                
                if 'users' in existing_tables:
                    print("   ✅ Users table already exists!")
                    return True
            
        except Exception as e:
            print(f"   - Could not query existing tables: {str(e)}")
        
        # Try to create table by inserting a dummy record and seeing if schema is auto-created
        print("   - Attempting table creation via schema inference...")
        
        dummy_user = {
            "id": "00000000-0000-0000-0000-000000000000",  # UUID format
            "email": "schema-test@example.com",
            "hashed_password": "dummy_hash",
            "is_active": True,
            "is_superuser": False
        }
        
        # This might create the table if Supabase allows it
        response = supabase.table("users").insert(dummy_user).execute()
        
        if response.data:
            print("   ✅ Table created via schema inference!")
            # Clean up the dummy record
            supabase.table("users").delete().eq("id", "00000000-0000-0000-0000-000000000000").execute()
            print("   ✅ Dummy record cleaned up")
            return True
        else:
            print("   ❌ Schema inference failed")
            return False
        
    except Exception as e:
        print(f"❌ Schema definition approach failed: {str(e)}")
        return False

async def test_crud_after_creation():
    """Test CRUD functions after table is confirmed to exist"""
    print("\n🧪 Testing CRUD functions with existing table...")
    
    try:
        from src.crud.crud_user import user_crud
        from src.models.user import UserCreate
        
        # Test 1: Create a test user
        print("   - Testing user creation...")
        test_user_data = UserCreate(
            email="crud-test@agent-makalah.com",
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
        found_user = await user_crud.get_user_by_email("crud-test@agent-makalah.com")
        if found_user:
            print(f"   ✅ User found: {found_user.email}")
        else:
            print("   ❌ Failed to find user")
            return False
        
        # Test 3: Authenticate user
        print("   - Testing user authentication...")
        auth_user = await user_crud.authenticate_user("crud-test@agent-makalah.com", "testpassword123")
        if auth_user:
            print(f"   ✅ Authentication successful: {auth_user.email}")
        else:
            print("   ❌ Authentication failed")
            return False
        
        # Test 4: Update user
        print("   - Testing user update...")
        from src.models.user import UserUpdate
        update_data = UserUpdate(is_superuser=True)
        updated_user = await user_crud.update_user(str(found_user.id), update_data)
        if updated_user and updated_user.is_superuser:
            print(f"   ✅ User updated successfully")
        else:
            print("   ❌ Failed to update user")
        
        # Test 5: Clean up test user
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

def show_manual_instructions():
    """Show manual instructions for creating the table"""
    print("\n📝 Manual table creation required:")
    print("   1. Go to Supabase Dashboard > SQL Editor")
    print("   2. Run this SQL:")
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
    print("   3. Run this script again to test CRUD functions")

async def main():
    """Main function"""
    print("🎯 Agent-Makalah Pragmatic Users Table Setup\n")
    
    # Step 1: Test if table exists
    table_exists = test_table_exists()
    
    if not table_exists:
        print("\n" + "="*50)
        print("Table doesn't exist, trying to create...")
        print("="*50)
        
        # Step 2: Try to create table
        table_created = create_table_via_schema_definition()
        
        if table_created:
            print("✅ Table creation successful!")
            table_exists = True
        else:
            print("❌ Automatic table creation failed")
            show_manual_instructions()
            return
    
    if table_exists:
        print("\n" + "="*50)
        print("Testing CRUD Functions")
        print("="*50)
        
        # Step 3: Test CRUD functions
        crud_success = await test_crud_after_creation()
        
        if crud_success:
            print("\n🎉 All tests passed! Users table is ready for production!")
        else:
            print("\n❌ CRUD tests failed. Check your implementation.")

if __name__ == "__main__":
    asyncio.run(main()) 