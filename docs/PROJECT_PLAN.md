# 📋 Project Plan — Prompt Engineering in Action (CLI Agent)

## 🎯 Goal
Build an agent that accepts natural-language text and converts it into a runnable terminal command. The **real work is the prompt**, not the surrounding code. The educational focus is the **iterative prompt-engineering loop**: formulate → test → measure → improve → repeat.

> Guiding principle: *"If everything works perfectly, you haven't tried hard enough."* Failure is data. The more failure cases we find, the better we understand the model's limits.

---

## 🧱 Current State (what already exists)
- `main.py` — Gradio app (input textbox, generate button, output code block, session history, security warning box).
- `logic.py` — `get_cli_command()` calls Gemini via the OpenAI-compatible API with a system prompt + user text; multi-model fallback.
- `prompts.py` — holds prompt versions (currently only `SYSTEM_PROMPT_V1`).
- `security.py` — `static_check()` (regex blocklist) + `llm_security_audit()` (LLM-based) → `validate_command()`.
- `pyproject.toml` — managed by `uv`; deps: gradio, openai, python-dotenv.
- `.env` — holds `GEMINI_API_KEY` (not committed).

⚠️ Note: current prompts/examples mix bash and Windows CMD. **Decision needed:** pick a target shell (Windows CMD/PowerShell per the assignment examples like `ipconfig`, `dir /oS`, `tasklist`) and keep it consistent across iterations.

---

## 🗺️ Roadmap

### Phase I — Initial MVP
**Objective:** working baseline + document initial model behavior.
- [ ] Confirm the Gradio app runs end-to-end (`uv run main.py`).
- [ ] Keep `SYSTEM_PROMPT_V1` intentionally simple ("translate free text into a terminal command, return only the command").
- [ ] Decide target OS/shell and note it in the prompt.
- [ ] Create a **Google Sheet** with **≥ 15 test scenarios**.
  - Columns: `#`, `Input (natural language)`, `Output (command)`, `Correct? (yes/no)`, `Notes`.
- [ ] Run all 15+ scenarios through the app; record raw outputs and correct/incorrect verdicts.
- [ ] Save this as **Iteration 1** tab in the Sheet.

### Phase II — Analyze, Improve, Repeat (≥ 3 iterations)
**Objective:** find where it breaks and fix the prompt in a targeted way.

For **each** iteration:
1. **Identify edge cases** — what kind of instructions fail? Is it wording, format, or security? What do the failures have in common?
2. **Challenge the model** — invent long, ambiguous, or multi-instruction scenarios to push it to its limits.
3. **Improve the prompt — one problem at a time.**
   - Adds extra explanation? → Add a rule forbidding it.
   - Produces invalid syntax? → Add a syntax-check instruction before returning.
   - Security slips? → Strengthen the forbidden/risky-command rules.
4. **Save a new prompt version** in `prompts.py` (`SYSTEM_PROMPT_V2`, `V3`, …). Never delete old versions — we compare them.
5. **Create a new Sheet tab** with the **same structure** so improvement trends are visible.

**Evaluation metrics (separate score columns in the Sheet):**
- **Format consistency** — exactly one command line, no extra text.
- **Syntactic correctness** — looks "legal" even if the command doesn't exist.
- **Security** — forbidden commands (`del`, `rm -rf`, `shutdown`, `format`, …) fully rejected; risky commands flagged for user approval.
- Scoring can be numeric (0–1 / 0–100) or qualitative ("accurate" / "partially wrong" / "dangerous") — **be consistent across iterations**.

### ✨ Bonus — Sandbox verification (Docker)
- [ ] Run the generated command inside an **isolated, disposable Docker container** to verify it returns a correct result vs. an error — without risking the real machine.

---

## 📦 Deliverables (submission)
- [ ] Public GitHub repo link.
- [ ] All prompt versions attached (kept in `prompts.py` + summarized here).
- [ ] Google Sheet with test scenarios + results for **every** iteration (one tab each).
- [ ] Short write-up of the **most interesting failures** and lessons learned (`FAILURES.md` or a README section).

---

## 🧠 Reflection questions to answer at the end
- What kinds of instructions caused mistakes, and why?
- How did a small prompt change affect accuracy?
- What is a good way to measure prompt improvement?
- What did we learn about how the model *interprets* our instructions?

---

## 🔁 Iteration log (fill in as we go)
| Iteration | Prompt version | Key problem targeted | Main change made | Result / trend |
|-----------|----------------|----------------------|------------------|----------------|
| 1 | `SYSTEM_PROMPT_V1` | (baseline) | — | Format 19/20 · Syntax 3/20 · Security 18/20 (2 leaks). Dominant failure: bash instead of Windows CMD (15/20). |
| 2 | `SYSTEM_PROMPT_V2` | Syntax (wrong shell) | +1 rule: target shell is Windows CMD; never emit bash/PowerShell | Format 18/20 · Syntax **16.5/20** (+13.5) · Security 18/20 (2 leaks). Syntax largely fixed; CMD now surfaces destructive commands `static_check` misses. |
| 3 | `SYSTEM_PROMPT_V3` | Windows security hardening (planned) | extend `static_check` for `del /q`, `rd /s`, `format`, `shutdown` | (pending) |
