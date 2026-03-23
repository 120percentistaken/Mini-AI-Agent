"""
main.py — FastAPI application entry point.

Defines the POST /chat endpoint that:
  - Accepts a user message
  - Passes it to the agent
  - Returns a structured JSON response
"""
from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio


from agent import run_agent

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Mini AI Agent",
    description="An internal chat assistant powered by Groq and FastAPI.",
    version="0.0.1",
    
)

# ---------------------------------------------------------------------------
# Request and Response schemas (Pydantic validates these automatically)
# ---------------------------------------------------------------------------



class ChatRequest(BaseModel):
    message: str  # The user's plain text message


class ChatResponse(BaseModel):
    reply: str          # The assistant's final text response
    tool_called: str | None  # Name of tool used, or null
    tool_result: dict | None  # Tool output, or null
    model: str          # Which LLM model was used


# ---------------------------------------------------------------------------
# POST /chat — main endpoint
# ---------------------------------------------------------------------------

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Accepts a user message and returns a structured AI response.

    Example request body:
        { "message": "What's the weather in Manila?" }

    Example response:
        {
          "reply": "It's currently 32°C and sunny in Manila!",
          "tool_called": "get_weather",
          "tool_result": { "city": "Manila", "temperature_c": 32, ... },
          "model": "gemini-1.5-flash"
        }
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        result = await asyncio.wait_for(
            run_agent(request.message),
            timeout=30.0  # Fail gracefully if LLM takes too long
        )
        return ChatResponse(**result)

    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Request timed out. Please try again.")

    except Exception as e:
        # In production you'd log this properly (e.g., with structlog or logging module)
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


# ---------------------------------------------------------------------------
# Health check — useful for verifying the server is up
# ---------------------------------------------------------------------------

@app.get("/health")
async def health():
    return {"status": "ok"}
