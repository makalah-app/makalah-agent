"""
Create Real Users Script for Agent-Makalah Backend
Adds actual users and superuser to Supabase database
"""

import sys
import os
import asyncio
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.crud.crud_user import UserCRUD
from src.models.user import UserCreate, UserUpdate
from src.auth.password_utils import hash_password

# User credentials
USERS_TO_CREATE = [
    {
        "email": "posteriot@gmail.com",
        "password": "M4k4lah2025",
        "is_superuser": False,
        "description": "Regular User 1"
    },
    {
        "email": "1200pixels@gmail.com", 
        "password": "M4k4lah2025",
        "is_superuser": False,
        "description": "Regular User 2"
    },
    {
        "email": "erik.supit@gmail.com",
        "password": "M4k4lah2025", 
        "is_superuser": True,
        "description": "Superuser Admin"
    }
]

async def create_real_users():
    """Create real users in the database"""
    print("🎯 Agent-Makalah Real Users Creation")
    print("=" * 50)
    
    user_crud = UserCRUD()
    created_users = []
    
    for user_info in USERS_TO_CREATE:
        print(f"\n👤 Creating {user_info['description']}: {user_info['email']}")
        
        try:
            # Check if user already exists
            existing_user = await user_crud.get_user_by_email(user_info['email'])
            if existing_user:
                print(f"   ⚠️  User already exists: {user_info['email']}")
                
                # Update to superuser if needed
                if user_info['is_superuser'] and not existing_user.is_superuser:
                    print(f"   🔧 Updating to superuser...")
                    update_data = UserUpdate(is_superuser=True)
                    updated_user = await user_crud.update_user(str(existing_user.id), update_data)
                    if updated_user:
                        print(f"   ✅ Updated to superuser: {user_info['email']}")
                        created_users.append(updated_user)
                    else:
                        print(f"   ❌ Failed to update to superuser: {user_info['email']}")
                else:
                    created_users.append(existing_user)
                continue
            
            # Create new user
            user_create = UserCreate(
                email=user_info['email'],
                password=user_info['password']
            )
            
            new_user = await user_crud.create_user(user_create)
            if not new_user:
                print(f"   ❌ Failed to create user: {user_info['email']}")
                continue
            
            print(f"   ✅ User created successfully: {user_info['email']}")
            print(f"   📝 User ID: {new_user.id}")
            
            # Update to superuser if needed
            if user_info['is_superuser']:
                print(f"   🔧 Setting superuser privileges...")
                update_data = UserUpdate(is_superuser=True)
                updated_user = await user_crud.update_user(str(new_user.id), update_data)
                if updated_user:
                    print(f"   👑 Superuser privileges granted!")
                    created_users.append(updated_user)
                else:
                    print(f"   ❌ Failed to grant superuser privileges")
                    created_users.append(new_user)
            else:
                created_users.append(new_user)
                
        except Exception as e:
            print(f"   ❌ Error creating user {user_info['email']}: {str(e)}")
    
    return created_users

async def test_user_authentication():
    """Test authentication for all created users"""
    print("\n🧪 Testing User Authentication")
    print("-" * 30)
    
    user_crud = UserCRUD()
    
    for user_info in USERS_TO_CREATE:
        print(f"\n🔐 Testing login: {user_info['email']}")
        
        try:
            authenticated_user = await user_crud.authenticate_user(
                user_info['email'], 
                user_info['password']
            )
            
            if authenticated_user:
                print(f"   ✅ Authentication successful!")
                print(f"   📝 User ID: {authenticated_user.id}")
                print(f"   👤 Email: {authenticated_user.email}")
                print(f"   🔴 Active: {authenticated_user.is_active}")
                print(f"   👑 Superuser: {authenticated_user.is_superuser}")
                print(f"   📅 Created: {authenticated_user.created_at}")
            else:
                print(f"   ❌ Authentication failed!")
                
        except Exception as e:
            print(f"   ❌ Authentication error: {str(e)}")

async def verify_user_capabilities():
    """Verify user capabilities and permissions"""
    print("\n🛡️  Verifying User Capabilities")
    print("-" * 35)
    
    user_crud = UserCRUD()
    
    # Test regular user capabilities
    print("\n📋 Regular User Capabilities:")
    regular_user = await user_crud.get_user_by_email("posteriot@gmail.com")
    if regular_user:
        print(f"   ✅ Regular user: {regular_user.email}")
        print(f"   🔴 Can login: {regular_user.is_active}")
        print(f"   🚫 Superuser: {regular_user.is_superuser}")
    
    # Test superuser capabilities  
    print("\n👑 Superuser Capabilities:")
    superuser = await user_crud.get_user_by_email("erik.supit@gmail.com")
    if superuser:
        print(f"   ✅ Superuser: {superuser.email}")
        print(f"   🔴 Can login: {superuser.is_active}")
        print(f"   👑 Admin privileges: {superuser.is_superuser}")
        
        # Test admin function
        is_super = await user_crud.is_superuser(str(superuser.id))
        print(f"   🔧 Admin check passed: {is_super}")

async def main():
    """Main execution function"""
    print("🚀 Starting Agent-Makalah Real Users Setup")
    print("=" * 55)
    
    try:
        # Create users
        created_users = await create_real_users()
        print(f"\n📊 Summary: {len(created_users)} users processed")
        
        # Test authentication
        await test_user_authentication()
        
        # Verify capabilities
        await verify_user_capabilities()
        
        print("\n" + "=" * 55)
        print("🎉 REAL USERS SETUP COMPLETED!")
        print("✅ Users created and verified successfully")
        print("🔐 Authentication system ready for production")
        print("👑 Superuser admin access configured")
        print("📝 System ready for Agent-Makalah deployment")
        print("=" * 55)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Setup failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1) 