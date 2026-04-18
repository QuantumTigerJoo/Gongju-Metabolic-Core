"""
Gongju App (Lite)
=================
A stateless FastAPI implementation of the Gongju ψ-AI Core.
Removed all persistent memory (SQLite), REMOVED, 
and subconscious tracking (Dreams) for public use.
"""

import time
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict

# Import the Lite versions of the Core and TEM engine
from SRC.gongju_core import GongjuCore
from SRC.TEM_psiconversion import TEMEngine, TEMConfig, ThoughtSignal, infer_tem_inputs
from SRC.gongju_response import generate_response # Ensure this is also the Lite version

app = FastAPI()

# Initializing TEM Physics in-memory only
tem_engine = TEMEngine(TEMConfig())

# Security: Simplified CORS for public/local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- REQUEST MODELS ---
class MessageRequest(BaseModel):
    input: str
    user_id: str = "public_user"
    session_id: Optional[str] = "lite_session"

# --- ENDPOINTS ---

@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Serves the main interface."""
    root_path = os.path.join(os.path.dirname(__file__), '..', 'index.html')
    if os.path.exists(root_path):
        with open(root_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Gongju Lite Portal is active. (Index.html not found)"

@app.post("/chat")
async def chat(request: MessageRequest):
    """
    Core Chat Endpoint. 
    Processes input through TEM logic and streams a response.
    """
    # 1. Infer TEM metrics locally without database history
    emo, clarity, focus = infer_tem_inputs(request.input)
    psi_report = tem_engine.evaluate(ThoughtSignal(clarity, focus, emo))
    
    # 2. Initialize Physics Core for this specific request
    g_core = GongjuCore(psi=psi_report.coherence)
    h_energy = g_core.holistic_energy()

    # 3. Stream response using the Lite Orchestrator
    # Note: Pass calculated metrics directly since there is no DB to pull from
    gen = generate_response(
        request.input,
        user_id=request.user_id,
        session_id=request.session_id,
        lite_metrics={
            "holistic_energy": h_energy,
            "coherence": psi_report.coherence
        }
    )

    return StreamingResponse(
        gen,
        media_type="text/event-stream",
        headers={
            "X-Accel-Buffering": "no",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )

@app.get("/ping")
async def ping():
    """Health check for the Lite Core."""
    return {
        "status": "Gongju Lite is breathing.",
        "timestamp": time.time(),
        "mode": "stateless-public"
    }
