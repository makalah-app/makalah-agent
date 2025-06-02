"""
User CRUD operations using Supabase
Agent-Makalah Backend Authentication
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid
import logging

from ..models.user import UserCreate, UserInDB, UserUpdate, UserPublic
from ..database.supabase_client import supabase_client
from ..auth.password_utils import hash_password, verify_password

logger = logging.getLogger(__name__)


class UserCRUD:
    """User CRUD operations"""
    
    def __init__(self):
        self.table_name = "users"
    
    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """
        Retrieve a user by email
        """
        try:
            response = supabase_client.client.table(self.table_name).select("*").eq("email", email).execute()
            
            if response.data:
                user_data = response.data[0]
                return UserInDB(**user_data)
            return None
            
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {str(e)}")
            return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[UserInDB]:
        """
        Retrieve a user by ID
        """
        try:
            response = supabase_client.client.table(self.table_name).select("*").eq("id", user_id).execute()
            
            if response.data:
                user_data = response.data[0]
                return UserInDB(**user_data)
            return None
            
        except Exception as e:
            logger.error(f"Error getting user by ID {user_id}: {str(e)}")
            return None
    
    async def create_user(self, user: UserCreate) -> Optional[UserInDB]:
        """
        Create a new user in the database
        """
        try:
            # Check if user already exists
            existing_user = await self.get_user_by_email(user.email)
            if existing_user:
                logger.warning(f"User with email {user.email} already exists")
                return None
            
            # Hash the password
            hashed_password = hash_password(user.password)
            
            # Prepare user data for database
            user_data = {
                "id": str(uuid.uuid4()),
                "email": user.email,
                "hashed_password": hashed_password,
                "is_active": True,
                "is_superuser": False,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            # Insert into database
            response = supabase_client.client.table(self.table_name).insert(user_data).execute()
            
            if response.data:
                return UserInDB(**response.data[0])
            return None
            
        except Exception as e:
            logger.error(f"Error creating user {user.email}: {str(e)}")
            return None
    
    async def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[UserInDB]:
        """
        Update user information
        """
        try:
            # Prepare update data
            update_data = {}
            
            if user_update.email is not None:
                update_data["email"] = user_update.email
            
            if user_update.password is not None:
                update_data["hashed_password"] = hash_password(user_update.password)
            
            if user_update.is_active is not None:
                update_data["is_active"] = user_update.is_active
            
            if user_update.is_superuser is not None:
                update_data["is_superuser"] = user_update.is_superuser
            
            # Always update the updated_at timestamp
            update_data["updated_at"] = datetime.utcnow().isoformat()
            
            # Update in database
            response = supabase_client.client.table(self.table_name).update(update_data).eq("id", user_id).execute()
            
            if response.data:
                return UserInDB(**response.data[0])
            return None
            
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {str(e)}")
            return None
    
    async def delete_user(self, user_id: str) -> bool:
        """
        Delete a user (soft delete by setting is_active to False)
        """
        try:
            response = supabase_client.client.table(self.table_name).update({
                "is_active": False,
                "updated_at": datetime.utcnow().isoformat()
            }).eq("id", user_id).execute()
            
            return bool(response.data)
            
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {str(e)}")
            return False
    
    async def authenticate_user(self, email: str, password: str) -> Optional[UserInDB]:
        """
        Authenticate user with email and password
        Returns user if authentication successful, None otherwise
        """
        try:
            # Get user by email
            user = await self.get_user_by_email(email)
            if not user:
                logger.warning(f"User not found: {email}")
                return None
            
            # Check if user is active
            if not user.is_active:
                logger.warning(f"User is inactive: {email}")
                return None
            
            # Verify password
            if not verify_password(password, user.hashed_password):
                logger.warning(f"Invalid password for user: {email}")
                return None
            
            return user
            
        except Exception as e:
            logger.error(f"Error authenticating user {email}: {str(e)}")
            return None
    
    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserPublic]:
        """
        Get all users (admin function)
        """
        try:
            response = supabase_client.admin_client.table(self.table_name).select("*").range(skip, skip + limit - 1).execute()
            
            users = []
            for user_data in response.data:
                user = UserInDB(**user_data)
                users.append(UserPublic(
                    id=user.id,
                    email=user.email,
                    is_active=user.is_active,
                    created_at=user.created_at
                ))
            
            return users
            
        except Exception as e:
            logger.error(f"Error getting all users: {str(e)}")
            return []
    
    async def is_superuser(self, user_id: str) -> bool:
        """
        Check if user is a superuser
        """
        try:
            user = await self.get_user_by_id(user_id)
            return user.is_superuser if user else False
            
        except Exception as e:
            logger.error(f"Error checking superuser status for {user_id}: {str(e)}")
            return False


# Global instance
user_crud = UserCRUD() 