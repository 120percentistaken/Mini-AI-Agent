"""
agent.py — This is where the AI actually "thinks".
 
It takes the user's message, sends it to Groq, and figures out
whether the model wants to look something up (tool call) or just answer directly.
If a tool gets called, it runs it and feeds the result back so Groq can
write a proper response. Either way, it returns a clean dict at the end.
"""
 
import os
import json
from groq import AsyncGroq
 
from tools import TOOL_DECLARATIONS, execute_tool
 
# Groq client — picks up the API key from the environment
client = AsyncGroq(api_key=os.environ["GROQ_API_KEY"])
 
MODEL_NAME = "llama-3.3-70b-versatile"
 
# Groq expects tools in this exact format — we just wrap each declaration
GROQ_TOOLS = [
    {"type": "function", "function": decl}
    for decl in TOOL_DECLARATIONS
]
 
# Tells the model who it is and when to use its tools
SYSTEM_PROMPT = """
You are a helpful internal company assistant. You help employees with:
- Weather information for travel planning
- Company FAQ questions (hours, refunds, shipping, contact info)
 
When the user asks about weather or company policies, use the appropriate tool.
For everything else, answer conversationally from your general knowledge.
Keep responses concise and friendly.
"""
 
 
async def run_agent(user_message: str) -> dict:
    """
    The main pipeline. Takes a user message and returns a response dict.
 
    Two possible paths:
      - Groq answers directly → one LLM call, done
      - Groq wants to call a tool → run the tool, send result back, second LLM call
    """
 
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]
 
    # First call — we give Groq the message and all available tools.
    # It'll either answer directly or tell us to call a tool.
    response = await client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=GROQ_TOOLS,
        tool_choice="auto",  # let the model decide — don't force it
    )
 
    tool_called = None
    tool_result = None
    first_message = response.choices[0].message
 
    if first_message.tool_calls:
        # Groq decided to use a tool — let's find out which one and run it
        tool_call = first_message.tool_calls[0]
        tool_called = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)
 
        tool_result = await execute_tool(tool_called, tool_args)
 
        # Now we feed the tool result back into the conversation so Groq
        # can use it to write a proper response for the user
        messages.append(first_message)  # what Groq said ("I want to call X")
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(tool_result),  # tool result has to be a string
        })
 
        # Second call — Groq now has the tool result and writes the final reply
        final_response = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
        )
 
        reply = final_response.choices[0].message.content
 
    else:
        # No tool needed — Groq answered from its own knowledge
        reply = first_message.content
 
    return {
        "reply": reply,
        "tool_called": tool_called,
        "tool_result": tool_result,
        "model": MODEL_NAME,
    }
 