"""
tools.py — Mock tool definitions for the AI agent.

Each tool has two parts:
  1. A declaration (dict) that tells the LLM what the tool does and what args it needs.
  2. An async function that actually executes the tool and returns a result.
"""

import random

# ---------------------------------------------------------------------------
# Tool declarations — these are sent to Gemini so it knows what tools exist
# ---------------------------------------------------------------------------

TOOL_DECLARATIONS = [
    {
        "name": "get_weather",
        "description": (
            "Returns the current weather for a given city. "
            "Call this whenever the user asks about weather or temperature."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The name of the city, e.g. 'Manila' or 'Tokyo'.",
                }
            },
            "required": ["city"],
        },
    },
    {
        "name": "get_faq_answer",
        "description": (
            "Looks up answers to frequently asked company questions. "
            "Call this when the user asks about policies, hours, or company info."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The FAQ question to look up.",
                }
            },
            "required": ["question"],
        },
    },
]

# ---------------------------------------------------------------------------
# Mock FAQ knowledge base
# ---------------------------------------------------------------------------

FAQ_KB = {
    "hours": "We are open Monday to Friday, 9 AM to 6 PM (PHT).",
    "refund": "Refunds are processed within 5–7 business days.",
    "contact": "You can reach support at support@company.com.",
    "shipping": "Standard shipping takes 3–5 business days.",
}


# ---------------------------------------------------------------------------
# Tool executor functions
# ---------------------------------------------------------------------------

async def get_weather(city: str) -> dict:
    """
    Mock weather tool. Returns fake but realistic weather data.
    In a real system, you'd call OpenWeatherMap or similar here.
    """
    conditions = ["Sunny", "Cloudy", "Rainy", "Partly cloudy", "Thunderstorms"]
    temp_c = random.randint(18, 38)

    return {
        "city": city,
        "temperature_c": temp_c,
        "temperature_f": round(temp_c * 9 / 5 + 32, 1),
        "condition": random.choice(conditions),
        "humidity_pct": random.randint(40, 95),
    }


async def get_faq_answer(question: str) -> dict:
    """
    Mock FAQ lookup. Searches a small in-memory knowledge base.
    In a real system, you'd query a database or vector store.
    """
    question_lower = question.lower()

    for keyword, answer in FAQ_KB.items():
        if keyword in question_lower:
            return {"question": question, "answer": answer, "found": True}

    return {
        "question": question,
        "answer": "Sorry, I don't have an answer for that specific question.",
        "found": False,
    }


# ---------------------------------------------------------------------------
# Dispatcher — routes tool name → correct async function
# ---------------------------------------------------------------------------

async def execute_tool(tool_name: str, tool_args: dict) -> dict:
    """
    Given a tool name and arguments (from the LLM), call the right function.
    Raises ValueError if the tool is not recognized.
    """
    if tool_name == "get_weather":
        return await get_weather(**tool_args)
    elif tool_name == "get_faq_answer":
        return await get_faq_answer(**tool_args)
    else:
        raise ValueError(f"Unknown tool: '{tool_name}'")
