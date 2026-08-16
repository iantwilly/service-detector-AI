from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import subprocess
import os
from typing import List, Dict, Any

# Import our custom modules
from gcp_scanner import list_projects, scan_project_resources
from cost_detector import analyze_cost

app = FastAPI(title="AI Cloud Cost Detective API")

# Enable CORS for http://localhost:5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProjectIdRequest(BaseModel):
    project_id: str

@app.get("/api/projects")
async def get_projects():
    """Get list of accessible GCP projects."""
    try:
        projects = list_projects()
        return {"projects": projects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze")
async def analyze_project(request: ProjectIdRequest):
    """Analyze a specific GCP project for cost insights."""
    try:
        # First, get resources for the project
        resources = scan_project_resources(request.project_id)
        # Then, analyze for cost
        analysis = analyze_cost(resources)
        return {"project_id": request.project_id, "analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)