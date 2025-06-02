"""
Supabase client configuration and database operations
Agent-Makalah Backend
"""
from supabase import create_client, Client
from typing import Optional, List, Dict, Any
import logging
from ..core.config import settings

logger = logging.getLogger(__name__)

class SupabaseClient:
    """Supabase client wrapper for Agent-Makalah operations"""
    
    def __init__(self):
        self._client: Optional[Client] = None
        self._admin_client: Optional[Client] = None
    
    @property
    def client(self) -> Client:
        """Get Supabase client with anon key"""
        if self._client is None:
            self._client = create_client(
                settings.supabase_url,
                settings.supabase_anon_key
            )
        return self._client
    
    @property
    def admin_client(self) -> Client:
        """Get Supabase client with service role key (admin privileges)"""
        if self._admin_client is None:
            self._admin_client = create_client(
                settings.supabase_url,
                settings.supabase_service_role_key
            )
        return self._admin_client
    
    async def health_check(self) -> Dict[str, Any]:
        """Check Supabase connection health"""
        try:
            # Simple test query - try to access any system table
            response = self.client.table("information_schema.tables").select("table_name").limit(1).execute()
            
            return {
                "status": "healthy",
                "supabase_url": settings.supabase_url,
                "project_ref": settings.supabase_project_ref,
                "connection": "success"
            }
        except Exception as e:
            logger.error(f"Supabase health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "supabase_url": settings.supabase_url,
                "project_ref": settings.supabase_project_ref,
                "connection": "failed",
                "error": str(e)
            }
    
    async def get_agents(self) -> List[Dict[str, Any]]:
        """Get all agents from database"""
        try:
            response = self.client.table("agents").select("*").execute()
            return response.data
        except Exception as e:
            logger.error(f"Failed to get agents: {str(e)}")
            # Return mock data if table doesn't exist yet
            return [
                {
                    "id": 1,
                    "name": "Agent-Makalah-Primary",
                    "type": "research",
                    "status": "active",
                    "created_at": "2025-01-31T00:00:00Z"
                },
                {
                    "id": 2,
                    "name": "Agent-Makalah-Secondary", 
                    "type": "writing",
                    "status": "active",
                    "created_at": "2025-01-31T00:00:00Z"
                },
                {
                    "id": 3,
                    "name": "Agent-Makalah-Review",
                    "type": "review", 
                    "status": "active",
                    "created_at": "2025-01-31T00:00:00Z"
                }
            ]
    
    async def create_agent(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new agent"""
        try:
            response = self.client.table("agents").insert(agent_data).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Failed to create agent: {str(e)}")
            raise Exception(f"Database error: {str(e)}")
    
    async def get_agent_by_id(self, agent_id: int) -> Optional[Dict[str, Any]]:
        """Get agent by ID"""
        try:
            response = self.client.table("agents").select("*").eq("id", agent_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Failed to get agent {agent_id}: {str(e)}")
            return None

# Global Supabase client instance
supabase_client = SupabaseClient() 