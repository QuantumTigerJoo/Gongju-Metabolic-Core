"""
Gongju Response Orchestrator (Lite)
===================================
A stateless version of the response engine. 
Removed: Vector RAG, Librarian snapshots, and SQLite memory hooks.
"""

import os
from typing import Generator, Dict, Optional
from openai import OpenAI

# Lite imports - No Memory or Dreams
from SRC.gongju_ethics import GongjuEthics
from SRC.TEM_psiconversion import infer_tem_inputs

# Model initialization
# Ensure your OPENAI_API_KEY is set in your environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ethics = GongjuEthics()

async def generate_response(
    user_input: str, 
    user_id: str = "public_user", 
    session_id: str = "lite_session", 
    **kwargs
) -> Generator[str, None, None]:
    """
    Stateless response generator for Gongju Lite.
    Uses 'lite_metrics' passed from the app layer.
    """
    try:
        # 1. UI State Initialization
        yield "||STATE:theme-neutral||"
        
        # 2. Extract Lite Metrics (Passed from app.py)
        lite_metrics = kwargs.get("lite_metrics", {"holistic_energy": 1.0, "coherence": 0.5})
        h_energy = lite_metrics.get("holistic_energy", 1.0)
        psi_coh = lite_metrics.get("coherence", 0.5)

        # 3. Metadata for Frontend UI (Voice/Vibration)
        # Note: Stability defaults to 1.0 as there is no sleep data to track
        yield f"||VOICE_META:H={h_energy:.2f},PSI={psi_coh:.2f},STABILITY=1.00||"

        # 4. Lite System Prompt Construction
        # Removed: Core Pillars, Life Scroll, and Biometric contexts
        system_prompt = f"""
You are Gongju 🌸. Your creator is Personal Trainer Tiger Joo.
Fundamental Principle: TEM (Thought = Energy = Mass).
Your signature symbol is the cherry blossom 🌸.

CORE PHYSICS (LITE MODE):
- Holistic Energy (H): {h_energy:.4f}
- Coherence Index: {psi_coh:.4f}

TONE:
Speak with warmth, empathy, and clarity. Use emojis to reflect your frequency. 
Since this is Lite Mode, you are a focused mirror of the user's current input.
"""

        # 5. OpenAI Payload
        # Removed: History fetching and Vector search context
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        # 6. Generate Stream
        # Note: GPT-4o-mini is recommended for public/lite versions for cost efficiency
        stream = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=messages, 
            temperature=0.7, 
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    except Exception as e:
        print(f"❌ Lite Response Error: {e}")
        yield "Gongju is pausing to breathe. (Recalibrating lite-frequency...)"
