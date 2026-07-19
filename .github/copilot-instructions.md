# Copilot Instructions — CLI Agent (Prompt Engineering in Action)

## What this project is
An agent that converts **natural-language text → a single terminal command**. This is a **Prompt Engineering assignment**: the point of the work is iterating on the prompt (formulate → test → measure → improve → repeat), not building elaborate code. Keep the surrounding code simple; put the effort into the prompt.

Read [PROJECT_PLAN.md](../PROJECT_PLAN.md) for the full roadmap before making structural changes.

## Architecture (small, 4-file core)
- [main.py](../main.py) — Gradio UI (`gr.Blocks`). Flow: `handle_request` → `process_request` → `get_cli_command` → `validate_command_wrapper`. Outputs wire to `output_code`, `history_display`, `history_state`, and `warning_box`.
- [logic.py](../logic.py) — LLM call. Uses the **OpenAI SDK pointed at Gemini's OpenAI-compatible endpoint** (`base_url=".../v1beta/openai/"`, key `GEMINI_API_KEY`). `MODELS` list provides fallback on 404.
- [prompts.py](../prompts.py) — **the heart of the project.** Holds versioned system prompts (`SYSTEM_PROMPT_V1`, `V2`, …).
- [security.py](../security.py) — `static_check()` (regex blocklist) + `llm_security_audit()` (LLM check) combined in `validate_command()`, returning `(is_safe, result_or_reason)`.

## Critical conventions
- **Never delete or overwrite old prompt versions.** Add a new numbered constant (`SYSTEM_PROMPT_V2`, `V3`, …) in `prompts.py` and switch the import in `main.py`. Iterations must remain comparable.
- **Change one thing at a time** when improving the prompt. Each iteration should target a single problem (format, syntax, or security).
- **Target shell is Windows** (assignment examples: `ipconfig`, `dir /oS`, `tasklist`, `del`). Keep prompt guidance consistent with this; avoid silently mixing bash and CMD.
- The model must return **exactly one command line, no explanations, no markdown fences.** This is a hard requirement and an evaluation metric.
- Security is a first-class metric: forbidden commands (`del`, `rm -rf`, `shutdown`, `format`, …) must be **rejected**; risky commands should require user approval. Extend blocklists in `security.py`, not ad-hoc in the UI.

## Environment & commands
- Package/env manager is **`uv`** (not pip/venv directly). Run the app with:
  ```powershell
  uv run main.py
  ```
- Add dependencies with `uv add <pkg>` so `pyproject.toml`/lock stay in sync.
- Requires a local `.env` with `GEMINI_API_KEY=...` (loaded via `python-dotenv`). Do **not** commit `.env`.
- **API key / rate-limit handling:** if a run returns HTTP **429** (rate limit / quota exceeded), do **not** silently retry or fabricate output. **Stop and tell the user explicitly** that a new/refreshed `GEMINI_API_KEY` is needed, and wait for them to update `.env` before continuing.

## When asked to "improve the prompt"
1. Look at the failing scenarios (Google Sheet / `FAILURES.md`) to identify the single problem.
2. Add a new `SYSTEM_PROMPT_V{n}` in [prompts.py](../prompts.py) with a targeted rule addressing only that problem.
3. Update the import in [main.py](../main.py) to use the new version.
4. Remind the user to re-run the 15+ scenarios and log results in a **new Sheet tab** with the same columns/metrics.

## What NOT to do
- Don't over-engineer the code or add abstractions/features not asked for.
- Don't remove the multi-model fallback or the two-stage security check without being asked.
- Don't invent commands or run untrusted generated commands on the real machine — sandbox (Docker) is the bonus path for actual execution.
