"""
Agent-Makalah Backend System
Main FastAPI application entry point

This is the core FastAPI application for the Agent-Makalah academic writing assistant.
It provides RESTful APIs for the multi-agent system that helps users create and analyze
academic papers in Bahasa Indonesia.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from typing import Dict, Any
import os
from datetime import datetime

# Import API routes
from api.routes import api_router

# Initialize FastAPI app
app = FastAPI(
    title="Agent-Makalah Backend API",
    description="AI-powered academic writing assistant for Bahasa Indonesia",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)

# Health check response model
class HealthResponse(BaseModel):
    status: str
    message: str
    timestamp: str
    version: str
    system: str

# Welcome response model
class WelcomeResponse(BaseModel):
    message: str
    description: str
    version: str
    endpoints: Dict[str, str]

@app.get("/", response_model=WelcomeResponse)
async def root():
    """
    Welcome endpoint for Agent-Makalah Backend API
    
    Returns basic information about the API and available endpoints.
    """
    return WelcomeResponse(
        message="Welcome to Agent-Makalah Backend API",
        description="AI-powered academic writing assistant designed for Bahasa Indonesia academic writing",
        version="1.0.0",
        endpoints={
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint for monitoring and deployment
    
    Returns the current status of the application and system information.
    """
    return HealthResponse(
        status="healthy",
        message="Agent-Makalah Backend is running successfully",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        system="Agent-Makalah Multi-Agent Academic Writing Assistant"
    )

@app.get("/api/v1/status")
async def api_status():
    """
    API status endpoint providing detailed system information
    """
    return {
        "api_version": "v1",
        "service": "agent-makalah-backend",
        "status": "operational",
        "features": {
            "new_paper_creation": "available",
            "document_analysis": "available", 
            "multi_agent_system": "available",
            "bahasa_indonesia_support": "available"
        },
        "agents": {
            "orchestrator": "ready",
            "brainstorming": "ready",
            "literature_search": "ready", 
            "outline_draft": "ready",
            "writer": "ready",
            "analysis_editor": "ready"
        }
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "Endpoint not found", "error": "Not Found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error", "error": "Server Error"}
    )

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 