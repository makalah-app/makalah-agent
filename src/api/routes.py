"""
Agent-Makalah Backend API Routes
Main API router configuration for all endpoints with Supabase integration
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
from pydantic import BaseModel
from src.database.supabase_client import supabase_client

# Create main API router
api_router = APIRouter(prefix="/api/v1")

# === Response Models ===

class AgentStatus(BaseModel):
    name: str
    status: str
    last_activity: str

class SystemInfo(BaseModel):
    total_agents: int
    active_sessions: int
    system_load: str
    uptime: str

# === API Endpoints ===

@api_router.get("/agents", response_model=List[AgentStatus])
async def get_agents_status():
    """
    Get status of all Agent-Makalah multi-agent system components
    """
    return [
        AgentStatus(name="Orchestrator_Agent", status="ready", last_activity="active"),
        AgentStatus(name="Brainstorming_Agent", status="ready", last_activity="idle"),
        AgentStatus(name="Literature_Search_Agent", status="ready", last_activity="idle"),
        AgentStatus(name="Outline_Draft_Agent", status="ready", last_activity="idle"),
        AgentStatus(name="Writer_Agent", status="ready", last_activity="idle"),
        AgentStatus(name="Analysis_Editor_Agent", status="ready", last_activity="idle"),
    ]

@api_router.get("/system", response_model=SystemInfo)
async def get_system_info():
    """
    Get detailed system information for Agent-Makalah backend with Supabase health
    """
    try:
        # Check Supabase health
        supabase_health = await supabase_client.health_check()
        
        return SystemInfo(
            total_agents=6,
            active_sessions=0,
            system_load="low" if supabase_health["status"] == "healthy" else "high",
            uptime="operational" if supabase_health["status"] == "healthy" else "degraded"
        )
    except Exception as e:
        return SystemInfo(
            total_agents=6,
            active_sessions=0,
            system_load="high",
            uptime="degraded"
        )

@api_router.post("/papers/new")
async def create_new_paper():
    """
    Initiate new academic paper creation workflow
    This will be implemented in future tasks with full multi-agent integration
    """
    return {
        "message": "New paper creation endpoint ready",
        "status": "not_implemented",
        "workflow": "multi_agent_paper_creation"
    }

@api_router.post("/papers/analyze")
async def analyze_existing_paper():
    """
    Analyze existing academic paper workflow
    This will be implemented in future tasks with document processing
    """
    return {
        "message": "Paper analysis endpoint ready", 
        "status": "not_implemented",
        "workflow": "document_analysis_feedback"
    }

@api_router.get("/database/health")
async def get_database_health():
    """
    Get Supabase database health status
    """
    try:
        health_status = await supabase_client.health_check()
        return {
            "database": "supabase",
            "health": health_status,
            "timestamp": "2025-01-31T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database health check failed: {str(e)}")

@api_router.get("/database/agents")
async def get_database_agents():
    """
    Get agents from Supabase database
    """
    try:
        agents = await supabase_client.get_agents()
        return {
            "agents": agents,
            "count": len(agents),
            "source": "supabase_database"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch agents from database: {str(e)}") 