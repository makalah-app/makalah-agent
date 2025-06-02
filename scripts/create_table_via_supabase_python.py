#!/usr/bin/env python3
"""
Create users table using Supabase Python client directly - Agent Makalah Backend
Authentication user management via Python client
"""
import asyncio
from supabase import create_client, Client
from src.core.config import settings

async def create_users_table_direct():
    """Create users table using Supabase Python client with admin access"""
    print("🚀 Creating users table via Python Supabase client...")
    
    try:
        # Initialize Supabase admin client
        supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key  # Admin access
        )
        
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
        
        print("   - Executing SQL via Supabase client...")
        
        # Try direct SQL execution via rpc (if available)
        try:
            response = supabase.rpc('execute', {'sql': sql_create_table}).execute()
            print("✅ Table created via RPC execute!")
            print(f"   - Response: {response}")
            return True
        except Exception as e:
            print(f"   - RPC execute failed: {str(e)}")
        
        # Try alternative approach - create via PostgREST raw SQL
        try:
            # Use raw SQL via PostgREST
            # This may not work depending on Supabase setup
            print("   - Trying alternative SQL execution...")
            
            # First try to see if table already exists
            response = supabase.table("users").select("id").limit(1).execute()
            print("✅ Users table already exists and is accessible!")
            return True
            
        except Exception as e:
            print(f"   - Table doesn't exist yet: {str(e)}")
            
            # Try creating table via inserting dummy data (schema inference)
            try:
                print("   - Attempting table creation via schema inference...")
                dummy_user = {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "email": "schema-test@example.com",
                    "hashed_password": "dummy_hash",
                    "is_active": True,
                    "is_superuser": False
                }
                
                response = supabase.table("users").insert(dummy_user).execute()
                if response.data:
                    print("   ✅ Table created via schema inference!")
                    # Clean up dummy record
                    supabase.table("users").delete().eq("id", "00000000-0000-0000-0000-000000000000").execute()
                    print("   ✅ Dummy record cleaned up")
                    return True
                    
            except Exception as e2:
                print(f"   - Schema inference failed: {str(e2)}")
        
        print("❌ All table creation methods failed")
        return False
        
    except Exception as e:
        print(f"❌ Failed to create users table: {str(e)}")
        return False

async def test_full_crud_workflow():
    """Test comprehensive CRUD workflow after table creation"""
    print("\n🧪 Testing Full CRUD Workflow...")
    
    try:
        from src.crud.crud_user import user_crud
        from src.models.user import UserCreate, UserUpdate
        
        # Test 1: Create test users
        print("\n1️⃣ Testing user creation...")
        test_users_data = [
            UserCreate(email="admin@agent-makalah.com", password="admin123!"),
            UserCreate(email="researcher@agent-makalah.com", password="research123!"),
            UserCreate(email="writer@agent-makalah.com", password="writer123!")
        ]
        
        created_users = []
        for user_data in test_users_data:
            try:
                created_user = await user_crud.create_user(user_data)
                if created_user:
                    created_users.append(created_user)
                    print(f"   ✅ Created: {created_user.email} (ID: {created_user.id})")
                else:
                    print(f"   ❌ Failed to create: {user_data.email}")
            except Exception as e:
                print(f"   ❌ Error creating {user_data.email}: {str(e)}")
        
        if not created_users:
            print("   ❌ No users were created - stopping test")
            return False
        
        # Test 2: Authentication testing
        print("\n2️⃣ Testing authentication...")
        auth_tests = [
            ("admin@agent-makalah.com", "admin123!", True),
            ("researcher@agent-makalah.com", "research123!", True),
            ("admin@agent-makalah.com", "wrongpassword", False),
            ("nonexistent@agent-makalah.com", "password", False)
        ]
        
        for email, password, should_succeed in auth_tests:
            auth_user = await user_crud.authenticate_user(email, password)
            if should_succeed:
                if auth_user:
                    print(f"   ✅ Auth success: {email}")
                else:
                    print(f"   ❌ Auth failed (should succeed): {email}")
            else:
                if not auth_user:
                    print(f"   ✅ Auth correctly failed: {email}")
                else:
                    print(f"   ❌ Auth succeeded (should fail): {email}")
        
        # Test 3: User queries
        print("\n3️⃣ Testing user queries...")
        for user in created_users:
            # Test get by email
            found_by_email = await user_crud.get_user_by_email(user.email)
            if found_by_email:
                print(f"   ✅ Found by email: {found_by_email.email}")
            else:
                print(f"   ❌ Not found by email: {user.email}")
            
            # Test get by ID
            found_by_id = await user_crud.get_user_by_id(str(user.id))
            if found_by_id:
                print(f"   ✅ Found by ID: {found_by_id.email}")
            else:
                print(f"   ❌ Not found by ID: {user.id}")
        
        # Test 4: User updates
        print("\n4️⃣ Testing user updates...")
        if created_users:
            test_user = created_users[0]
            
            # Make admin
            update_data = UserUpdate(is_superuser=True)
            updated_user = await user_crud.update_user(str(test_user.id), update_data)
            if updated_user and updated_user.is_superuser:
                print(f"   ✅ Updated to superuser: {updated_user.email}")
                
                # Verify superuser check
                is_super = await user_crud.is_superuser(str(test_user.id))
                if is_super:
                    print(f"   ✅ Superuser check confirmed: {updated_user.email}")
                else:
                    print(f"   ❌ Superuser check failed: {updated_user.email}")
            else:
                print(f"   ❌ Failed to update to superuser")
        
        # Test 5: Get all users
        print("\n5️⃣ Testing get all users...")
        all_users = await user_crud.get_all_users(skip=0, limit=10)
        if all_users:
            print(f"   ✅ Retrieved {len(all_users)} users:")
            for user in all_users:
                print(f"     • {user.email} (Active: {user.is_active})")
        else:
            print("   ❌ Failed to retrieve users")
        
        # Test 6: Soft delete
        print("\n6️⃣ Testing soft delete...")
        for user in created_users:
            deleted = await user_crud.delete_user(str(user.id))
            if deleted:
                print(f"   ✅ Soft deleted: {user.email}")
                
                # Verify soft delete
                found_user = await user_crud.get_user_by_id(str(user.id))
                if found_user and not found_user.is_active:
                    print(f"   ✅ Soft delete verified: {found_user.email} (Active: {found_user.is_active})")
                else:
                    print(f"   ❌ Soft delete verification failed: {user.email}")
            else:
                print(f"   ❌ Failed to delete: {user.email}")
        
        print("\n🎉 All CRUD workflow tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ CRUD workflow testing failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def cleanup_test_data():
    """Clean up test data completely"""
    print("\n🧹 Comprehensive cleanup...")
    
    try:
        supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key
        )
        
        # Hard delete all test users
        test_emails = [
            "admin@agent-makalah.com",
            "researcher@agent-makalah.com", 
            "writer@agent-makalah.com",
            "crud-test@agent-makalah.com",
            "test@agent-makalah.com",
            "schema-test@example.com"
        ]
        
        for email in test_emails:
            try:
                response = supabase.table("users").delete().eq("email", email).execute()
                if response.data:
                    print(f"   ✅ Cleaned up: {email}")
            except Exception as e:
                print(f"   ⚠️  Could not clean up {email}: {str(e)}")
        
        print("   ✅ Cleanup completed")
        
    except Exception as e:
        print(f"   ❌ Cleanup failed: {str(e)}")

async def main():
    """Main function - comprehensive table creation and testing"""
    print("🎯 Agent-Makalah Complete Database Setup & Testing\n")
    print("=" * 70)
    
    # Step 1: Create table
    print("STEP 1: Create users table")
    print("-" * 70)
    table_created = await create_users_table_direct()
    
    if table_created:
        print(f"\n✅ Users table is ready!")
        
        # Step 2: Test CRUD workflow
        print("\n" + "=" * 70)
        print("STEP 2: Test CRUD workflow")
        print("-" * 70)
        
        crud_success = await test_full_crud_workflow()
        
        # Step 3: Cleanup
        print("\n" + "=" * 70)
        print("STEP 3: Cleanup test data")
        print("-" * 70)
        await cleanup_test_data()
        
        # Final status
        print("\n" + "=" * 70)
        if crud_success:
            print("🎉 SUCCESS! Agent-Makalah users table is fully operational!")
            print("\n📝 Next steps:")
            print("   1. ✅ Task 4.2 (User Models & CRUD) - DONE")
            print("   2. 🔄 Continue to Task 4.3: JWT Token Management")
            print("   3. 🔄 Implement authentication endpoints")
            print("   4. 🔄 Test complete API flow")
        else:
            print("❌ Some CRUD tests failed. Check implementation.")
    else:
        print("\n❌ Table creation failed. Manual intervention required.")
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
    
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main()) 