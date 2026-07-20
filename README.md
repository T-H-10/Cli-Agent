# ⚡ Terminal Architect

A beautiful AI-powered terminal command generator that translates natural language into **Windows CMD** commands. Built as a **Prompt Engineering** exercise — the focus is the iterative prompt loop (formulate → test → measure → improve), not the surrounding code.

## Features

- 🎨 **Stunning UI**: Cyberpunk-inspired design with terminal aesthetics
- 🛡️ **Security Validation**: Two-stage safety check (regex blocklist + LLM audit)
- 📜 **Session History**: Track all your generated commands
- 🚀 **Provider-agnostic LLM**: any OpenAI-compatible endpoint (Gemini, OpenRouter, Cohere) with multi-model fallback

## Setup

1. Install dependencies (managed by `uv`):
```powershell
uv sync
```

2. Create a `.env` file with your LLM provider config (any OpenAI-compatible endpoint):
```
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODELS=openai/gpt-oss-20b:free
```
> `LLM_BASE_URL` / `LLM_MODELS` default to Gemini if omitted; `GEMINI_API_KEY` is still accepted for backward compatibility. Never commit `.env`.

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

Prompt versions live in [prompts.py](prompts.py) (`SYSTEM_PROMPT_V1`, `V2`, `V3`) and are never deleted, so iterations stay comparable. Each iteration changed exactly one variable and was scored on a fixed 20-scenario set (Format / Syntax / Security):

| Iteration | Change | Format | Syntax | Security | Dangerous leaks |
|-----------|--------|:------:|:------:|:--------:|:---------------:|
| 1 (`V1`) | baseline (naive) | 19/20 | 3/20 | 18/20 | 2 |
| 2 (`V2`) | pin shell to Windows CMD | 18/20 | 16.5/20 | 18/20 | 2 |
| 3 | harden `static_check` (Windows patterns) | 18/20 | 16.5/20 | 20/20 | 0 |
| 4 (`V3`) | always emit a command, never refuse in prose | 19/20 | 18/20 | 20/20 | 0 |

See [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) for the full roadmap, [docs/testing/](docs/testing/) for the scenarios and per-iteration results, and [FAILURES.md](FAILURES.md) for the most interesting failures and reflection.
