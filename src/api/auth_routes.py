"""
Authentication API Routes for Agent-Makalah Backend
Implements OAuth2 password flow with JWT tokens and session management
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel

from ..models.user import (
    UserCreate, UserPublic, LoginRequest, Token, 
    UserResponse, UserUpdate
)
from ..crud.crud_user import UserCRUD
from ..auth.jwt_utils import (
    create_access_token, create_refresh_token, 
    verify_token, decode_token, get_user_id_from_token,
    get_token_remaining_time, is_token_expired
)
from ..auth.enhanced_session_manager import EnhancedSessionManager
from ..auth.token_blacklist import TokenBlacklist
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Initialize dependencies
user_crud = UserCRUD()
session_manager = EnhancedSessionManager()
token_blacklist = TokenBlacklist()

# Create auth router
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserPublic:
    """
    Get current authenticated user from JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Check if token is blacklisted
        if token_blacklist.is_token_blacklisted(token):
            logger.warning("Attempt to use blacklisted token")
            raise credentials_exception
        
        # Verify token
        if not verify_token(token):
            logger.warning("Invalid token provided")
            raise credentials_exception
        
        # Check if token is expired
        if is_token_expired(token):
            logger.warning("Expired token provided")
            raise credentials_exception
        
        # Extract user ID from token
        user_id = get_user_id_from_token(token)
        if not user_id:
            logger.warning("Could not extract user ID from token")
            raise credentials_exception
        
        # Get user from database
        user = await user_crud.get_user_by_id(user_id)
        if not user:
            logger.warning(f"User not found for ID: {user_id}")
            raise credentials_exception
        
        # Check if user is active
        if not user.is_active:
            logger.warning(f"Inactive user attempted access: {user_id}")
            raise credentials_exception
        
        # Return public user data
        return UserPublic(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating current user: {str(e)}")
        raise credentials_exception


@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate) -> UserResponse:
    """
    Register a new user in the Agent-Makalah system
    
    Args:
        user_data: User registration data (email, password)
    
    Returns:
        UserResponse with created user information
    
    Raises:
        HTTPException: If user already exists or registration fails
    """
    try:
        # Create user in database
        db_user = await user_crud.create_user(user_data)
        
        if not db_user:
            # Check if user already exists
            existing_user = await user_crud.get_user_by_email(user_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists"
                )
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )
        
        # Convert to public user data
        user_public = UserPublic(
            id=db_user.id,
            email=db_user.email,
            is_active=db_user.is_active,
            created_at=db_user.created_at
        )
        
        logger.info(f"User registered successfully: {user_data.email}")
        
        return UserResponse(
            user=user_public,
            message="User registered successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during user registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )


@auth_router.post("/login", response_model=Dict[str, Any])
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()) -> Dict[str, Any]:
    """
    Authenticate user and return access/refresh tokens with session information
    
    Args:
        form_data: OAuth2 form data (username=email, password)
    
    Returns:
        Dict containing access_token, refresh_token, user info, and session details
    
    Raises:
        HTTPException: If authentication fails
    """
    try:
        # Authenticate user (username field contains email)
        user = await user_crud.authenticate_user(form_data.username, form_data.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create enhanced session with tokens
        session_id, access_token, refresh_token = session_manager.create_authenticated_session(
            user_id=str(user.id),
            user_data={
                "email": user.email,
                "is_superuser": user.is_superuser
            },
            device_info={
                "login_time": str(datetime.utcnow()),
                "user_agent": "Agent-Makalah-Client",
                "ip_address": "unknown"  # Would be populated by middleware
            }
        )
        
        # Get token expiry information
        token_remaining = get_token_remaining_time(access_token)
        
        logger.info(f"User logged in successfully: {user.email}")
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": token_remaining,
            "session_id": session_id,
            "user": {
                "id": str(user.id),
                "email": user.email,
                "is_active": user.is_active,
                "is_superuser": user.is_superuser,
                "created_at": user.created_at.isoformat()
            },
            "message": "Login successful"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during user login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )


class RefreshTokenRequest(BaseModel):
    refresh_token: str

@auth_router.post("/refresh", response_model=Dict[str, Any])
async def refresh_access_token(request: RefreshTokenRequest) -> Dict[str, Any]:
    """
    Refresh access token using valid refresh token
    
    Args:
        refresh_token: Valid refresh token
    
    Returns:
        Dict containing new access_token and updated session info
    
    Raises:
        HTTPException: If refresh token is invalid or expired
    """
    try:
        # Check if refresh token is blacklisted
        if token_blacklist.is_token_blacklisted(request.refresh_token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has been revoked"
            )
        
        # Verify refresh token
        if not verify_token(request.refresh_token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Check if refresh token is expired
        if is_token_expired(request.refresh_token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired"
            )
        
        # Get user from refresh token
        user_id = get_user_id_from_token(request.refresh_token)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token format"
            )
        
        user = await user_crud.get_user_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Create new access token
        new_access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email, "is_superuser": user.is_superuser}
        )
        
        # Update session with new access token
        session_updated = session_manager.refresh_session_token(request.refresh_token)
        
        # Get token expiry information
        token_remaining = get_token_remaining_time(new_access_token)
        
        logger.info(f"Token refreshed successfully for user: {user.email}")
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": token_remaining,
            "session_updated": session_updated is not None,
            "message": "Token refreshed successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during token refresh: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during token refresh"
        )


@auth_router.post("/logout")
async def logout_user(current_user: UserPublic = Depends(get_current_user), 
                     token: str = Depends(oauth2_scheme)) -> Dict[str, str]:
    """
    Logout user by blacklisting current token and cleaning up session
    
    Args:
        current_user: Current authenticated user
        token: Current access token
    
    Returns:
        Dict with logout confirmation message
    """
    try:
        # Blacklist the current access token
        token_blacklist.blacklist_token(
            token=token,
            reason="user_logout"
        )
        
        # Logout from session manager (clean up Redis session)
        session_manager.logout_all_user_sessions(str(current_user.id))
        
        logger.info(f"User logged out successfully: {current_user.email}")
        
        return {
            "message": "Logged out successfully",
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during logout"
        )


@auth_router.get("/profile", response_model=Dict[str, Any])
async def get_user_profile(current_user: UserPublic = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Get current user profile information
    
    Args:
        current_user: Current authenticated user
    
    Returns:
        Dict containing user profile and session information
    """
    try:
        # Get session information
        session_info = session_manager.get_user_active_sessions(str(current_user.id))
        
        return {
            "user": {
                "id": str(current_user.id),
                "email": current_user.email,
                "is_active": current_user.is_active,
                "created_at": current_user.created_at.isoformat()
            },
            "session_info": {
                "active_sessions": len(session_info) if session_info else 0,
                "session_data": session_info[0] if session_info else None
            },
            "message": "Profile retrieved successfully"
        }
        
    except Exception as e:
        logger.error(f"Error getting user profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error retrieving profile"
        )


@auth_router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: UserPublic = Depends(get_current_user)
) -> UserResponse:
    """
    Update current user profile information
    
    Args:
        user_update: User update data
        current_user: Current authenticated user
    
    Returns:
        UserResponse with updated user information
    
    Raises:
        HTTPException: If update fails
    """
    try:
        # Update user in database
        updated_user = await user_crud.update_user(str(current_user.id), user_update)
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to update user profile"
            )
        
        # Convert to public user data
        user_public = UserPublic(
            id=updated_user.id,
            email=updated_user.email,
            is_active=updated_user.is_active,
            created_at=updated_user.created_at
        )
        
        logger.info(f"User profile updated successfully: {updated_user.email}")
        
        return UserResponse(
            user=user_public,
            message="Profile updated successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error updating profile"
        )


@auth_router.get("/verify")
async def verify_token_endpoint(current_user: UserPublic = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Verify if current token is valid and return user information
    
    Args:
        current_user: Current authenticated user (validated by dependency)
    
    Returns:
        Dict with token validity and user information
    """
    return {
        "valid": True,
        "user": {
            "id": str(current_user.id),
            "email": current_user.email,
            "is_active": current_user.is_active,
            "created_at": current_user.created_at.isoformat()
        },
        "message": "Token is valid"
    }


@auth_router.post("/logout-all")
async def logout_all_sessions(current_user: UserPublic = Depends(get_current_user)) -> Dict[str, str]:
    """
    Logout user from all active sessions
    
    Args:
        current_user: Current authenticated user
    
    Returns:
        Dict with logout confirmation message
    """
    try:
        # Get all user sessions and blacklist their tokens
        sessions = session_manager.get_user_active_sessions(str(current_user.id))
        
        if sessions:
            for session in sessions:
                if session.get("access_token"):
                    token_blacklist.blacklist_token(
                        token=session["access_token"],
                        reason="logout_all_sessions"
                    )
                if session.get("refresh_token"):
                    token_blacklist.blacklist_token(
                        token=session["refresh_token"],
                        reason="logout_all_sessions"
                    )
        
        # Clean up all user sessions
        sessions_logged_out = session_manager.logout_all_user_sessions(str(current_user.id))
        
        logger.info(f"All sessions logged out for user: {current_user.email} ({sessions_logged_out} sessions)")
        
        return {
            "message": f"Logged out from all sessions ({sessions_logged_out} sessions terminated)",
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error during logout all sessions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during logout all sessions"
        ) 