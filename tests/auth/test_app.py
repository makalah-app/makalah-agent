"""
Simple FastAPI app for testing authentication endpoints
Avoids import issues by creating a minimal app instance
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create simple test app
app = FastAPI(title="Agent-Makalah Test API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include auth router
from src.api.auth_routes import auth_router

app.include_router(auth_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Agent-Makalah Test API"}

@app.get("/health")
async def health():
    return {"status": "healthy"} 