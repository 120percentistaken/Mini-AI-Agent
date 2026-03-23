# Mini AI Agent

A small AI-powered chat assistant built with FastAPI and Groq. You send it a message, it figures out whether to look something up or just answer directly, and returns a clean JSON response.

Built as a technical assessment. Kept simple on purpose.

---

## What it does

You hit one endpoint — `POST /chat` — with a message like *"What's the weather in Manila?"* and the agent decides whether to use a tool or answer from its own knowledge. The response always tells you what tool was used (if any) and what it returned.

It has two mock tools:
- **get_weather** — returns fake weather data for any city
- **get_faq_answer** — looks up answers to common company questions like hours, refunds, and shipping

---

## Project structure

```
mini-agent/
├── main.py          # The API — one endpoint, request/response handling
├── agent.py         # The AI logic — talks to Groq, handles tool calls
├── tools.py         # The tools — what they do and how they run
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Getting started

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd mini-agent
```

### 2. Create a virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` appear at the start of your terminal line.

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Get a free Groq API key

Go to https://console.groq.com/keys, sign up (no credit card needed), and create a key.

### 5. Create your `.env` file

```powershell
copy .env.example .env
```

Open `.env` and paste your key:

```
GROQ_API_KEY=gsk_your_key_here
```

### 6. Run it

```powershell
python -m uvicorn main:app --reload
```

That's it. Server is live at http://127.0.0.1:8000.

---

## Try it out

Head to http://127.0.0.1:8000/docs for an interactive UI where you can send test messages directly in the browser. No curl needed.

Some messages worth trying:
- `"What's the weather in Manila?"` — triggers the weather tool
- `"What are your business hours?"` — triggers the FAQ tool
- `"What is Python?"` — answered directly, no tool used

---

## Example responses

**Weather question:**
```json
{
  "reply": "It's currently 32°C and sunny in Manila, with humidity around 74%.",
  "tool_called": "get_weather",
  "tool_result": {
    "city": "Manila",
    "temperature_c": 32,
    "temperature_f": 89.6,
    "condition": "Sunny",
    "humidity_pct": 74
  },
  "model": "llama-3.3-70b-versatile"
}
```

**General question:**
```json
{
  "reply": "Python is a high-level programming language known for its simplicity and readability.",
  "tool_called": null,
  "tool_result": null,
  "model": "llama-3.3-70b-versatile"
}
```

---

## Environment variables

| Variable       | Required | Where to get it                  |
|----------------|----------|----------------------------------|
| `GROQ_API_KEY` | Yes      | https://console.groq.com/keys    |

---