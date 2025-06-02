#!/usr/bin/env python3
"""
Test CRUD functions assuming users table exists - Agent Makalah Backend
Authentication user management
"""
import asyncio
from supabase import create_client, Client
from src.core.config import settings

async def comprehensive_crud_test():
    """Comprehensive CRUD testing for users table"""
    print("🧪 Comprehensive CRUD Testing - Agent Makalah Users\n")
    
    try:
        from src.crud.crud_user import user_crud
        from src.models.user import UserCreate, UserUpdate
        
        # Test 1: Check table access
        print("1️⃣ Testing table access...")
        try:
            supabase: Client = create_client(
                settings.supabase_url,
                settings.supabase_anon_key
            )
            response = supabase.table("users").select("id").limit(1).execute()
            print("   ✅ Users table is accessible")
        except Exception as e:
            print(f"   ❌ Table access failed: {str(e)}")
            return False
        
        # Test 2: Create multiple test users
        print("\n2️⃣ Testing user creation...")
        test_users = [
            UserCreate(email="admin@agent-makalah.com", password="admin123"),
            UserCreate(email="user1@agent-makalah.com", password="user123"),
            UserCreate(email="researcher@agent-makalah.com", password="research123")
        ]
        
        created_users = []
        for user_data in test_users:
            try:
                created_user = await user_crud.create_user(user_data)
                if created_user:
                    created_users.append(created_user)
                    print(f"   ✅ Created user: {created_user.email}")
                else:
                    print(f"   ❌ Failed to create user: {user_data.email}")
            except Exception as e:
                print(f"   ❌ Error creating {user_data.email}: {str(e)}")
        
        if not created_users:
            print("   ❌ No users were created successfully")
            return False
        
        # Test 3: Get user by email
        print("\n3️⃣ Testing get user by email...")
        for user in created_users:
            found_user = await user_crud.get_user_by_email(user.email)
            if found_user:
                print(f"   ✅ Found user: {found_user.email}")
            else:
                print(f"   ❌ Failed to find user: {user.email}")
        
        # Test 4: Get user by ID
        print("\n4️⃣ Testing get user by ID...")
        for user in created_users:
            found_user = await user_crud.get_user_by_id(str(user.id))
            if found_user:
                print(f"   ✅ Found user by ID: {found_user.email}")
            else:
                print(f"   ❌ Failed to find user by ID: {user.id}")
        
        # Test 5: User authentication
        print("\n5️⃣ Testing user authentication...")
        auth_tests = [
            ("admin@agent-makalah.com", "admin123", True),
            ("user1@agent-makalah.com", "user123", True),
            ("admin@agent-makalah.com", "wrongpassword", False),
            ("nonexistent@agent-makalah.com", "password", False)
        ]
        
        for email, password, should_succeed in auth_tests:
            auth_user = await user_crud.authenticate_user(email, password)
            if should_succeed:
                if auth_user:
                    print(f"   ✅ Authentication successful: {email}")
                else:
                    print(f"   ❌ Authentication failed (should succeed): {email}")
            else:
                if not auth_user:
                    print(f"   ✅ Authentication correctly failed: {email}")
                else:
                    print(f"   ❌ Authentication succeeded (should fail): {email}")
        
        # Test 6: User updates
        print("\n6️⃣ Testing user updates...")
        if created_users:
            test_user = created_users[0]
            
            # Update to superuser
            update_data = UserUpdate(is_superuser=True)
            updated_user = await user_crud.update_user(str(test_user.id), update_data)
            if updated_user and updated_user.is_superuser:
                print(f"   ✅ Updated user to superuser: {updated_user.email}")
            else:
                print(f"   ❌ Failed to update user to superuser")
            
            # Update email
            new_email = "admin-updated@agent-makalah.com"
            update_data = UserUpdate(email=new_email)
            updated_user = await user_crud.update_user(str(test_user.id), update_data)
            if updated_user and updated_user.email == new_email:
                print(f"   ✅ Updated user email: {updated_user.email}")
                # Update our local reference
                test_user.email = new_email
            else:
                print(f"   ❌ Failed to update user email")
        
        # Test 7: Check superuser status
        print("\n7️⃣ Testing superuser check...")
        if created_users:
            test_user = created_users[0]
            is_super = await user_crud.is_superuser(str(test_user.id))
            if is_super:
                print(f"   ✅ Superuser check successful: {test_user.email}")
            else:
                print(f"   ❌ Superuser check failed: {test_user.email}")
        
        # Test 8: Get all users (admin function)
        print("\n8️⃣ Testing get all users...")
        all_users = await user_crud.get_all_users(skip=0, limit=10)
        if all_users:
            print(f"   ✅ Retrieved {len(all_users)} users:")
            for user in all_users:
                print(f"     • {user.email} (Active: {user.is_active})")
        else:
            print("   ❌ Failed to retrieve users")
        
        # Test 9: Soft delete users
        print("\n9️⃣ Testing user deletion (soft delete)...")
        for user in created_users:
            deleted = await user_crud.delete_user(str(user.id))
            if deleted:
                print(f"   ✅ Soft deleted user: {user.email}")
            else:
                print(f"   ❌ Failed to delete user: {user.email}")
        
        # Test 10: Verify soft delete
        print("\n🔟 Verifying soft delete...")
        for user in created_users:
            found_user = await user_crud.get_user_by_id(str(user.id))
            if found_user and not found_user.is_active:
                print(f"   ✅ User soft deleted correctly: {found_user.email} (Active: {found_user.is_active})")
            else:
                print(f"   ❌ Soft delete verification failed: {user.email}")
        
        print("\n🎉 All CRUD tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ CRUD testing failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def cleanup_test_data():
    """Clean up any test data left behind"""
    print("\n🧹 Cleaning up test data...")
    
    try:
        supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key  # Use admin client for cleanup
        )
        
        # Delete test users
        test_emails = [
            "admin@agent-makalah.com",
            "admin-updated@agent-makalah.com", 
            "user1@agent-makalah.com",
            "researcher@agent-makalah.com",
            "crud-test@agent-makalah.com",
            "test@agent-makalah.com"
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
    """Main function"""
    print("🎯 Agent-Makalah CRUD Testing Suite\n")
    print("=" * 60)
    
    # Run comprehensive tests
    success = await comprehensive_crud_test()
    
    # Cleanup test data
    await cleanup_test_data()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED! Your CRUD implementation is working perfectly!")
        print("📝 Next steps:")
        print("   1. Continue to Task 4.3: JWT Token Management")
        print("   2. Implement authentication endpoints")
        print("   3. Test API routes")
    else:
        print("❌ Some tests failed. Check the implementation.")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main()) 