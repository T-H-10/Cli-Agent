# ⚡ Terminal Architect

A beautiful AI-powered terminal command generator that translates natural language into **Windows CMD** commands. Built as a **Prompt Engineering** exercise — the focus is the iterative prompt loop (formulate → test → measure → improve), not the surrounding code.

## Features

- 🎨 **Stunning UI**: Cyberpunk-inspired design with terminal aesthetics
- 🛡️ **Security Validation**: Two-stage safety check (regex blocklist + LLM audit)
- 📜 **Session History**: Track all your generated commands
- 🚀 **Powered by Gemini AI**: Multiple model fallback support

## Setup

1. Install dependencies (managed by `uv`):
```powershell
uv sync
```

2. Create a `.env` file and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

3. Run the application:
```powershell
uv run main.py
```

## Usage

Simply describe what you want to do in natural language, and Terminal Architect will generate the appropriate **Windows CMD** command for you!

**Example inputs:**
- "List the files in the current folder" → `dir`
- "Show my IP configuration in full detail" → `ipconfig /all`
- "Show all running processes" → `tasklist`
- "List files sorted by size, smallest first" → `dir /oS`

## Prompt engineering

Prompt versions live in [prompts.py](prompts.py) (`SYSTEM_PROMPT_V1`, `V2`, …) and are never deleted, so iterations stay comparable. See [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) for the full roadmap and [docs/testing/](docs/testing/) for the test scenarios and per-iteration results.
