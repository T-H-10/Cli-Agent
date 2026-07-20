import os
from dotenv import load_dotenv
from openai import OpenAI
from security import validate_command

load_dotenv()

# --- Provider config (all OpenAI-compatible endpoints) --------------------
# Switch providers purely via .env, no code changes needed:
#   OpenRouter -> LLM_BASE_URL=https://openrouter.ai/api/v1
#   Cohere     -> LLM_BASE_URL=https://api.cohere.ai/compatibility/v1
#   Gemini     -> LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
# LLM_API_KEY is preferred; GEMINI_API_KEY is kept for backward compatibility.
API_KEY = os.environ.get("LLM_API_KEY") or os.environ.get("GEMINI_API_KEY")

BASE_URL = os.environ.get(
    "LLM_BASE_URL",
    "https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Comma-separated list in .env, e.g.
#   LLM_MODELS=deepseek/deepseek-chat-v3-0324:free,meta-llama/llama-3.3-70b-instruct:free
_default_models = "gemini-2.5-flash-lite,gemini-2.0-flash"
MODELS = [m.strip() for m in os.environ.get("LLM_MODELS", _default_models).split(",") if m.strip()]

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

# Name of the model that produced the most recent successful command
# (lets callers verify every answer came from the same model).
LAST_MODEL_USED = None

def get_cli_command(user_text, prompt_version, history):
    """
    sending ChatCompletion request to the LLM with the System prompt and the user input.
    """
    global LAST_MODEL_USED
    last_error = ""
    for model_name in MODELS:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": prompt_version},
                    {"role": "user", "content": user_text}
                ]
            )
            command = response.choices[0].message.content.strip()
            LAST_MODEL_USED = model_name

            history.append({"role": "user", "content": user_text})
            history.append({"role": "assistant", "content": command})
            
            return command, history
        
        except Exception as e:
            last_error = str(e)
            if "404" in last_error:
                print(f"Model {model_name} not found, trying next...")
                continue
            if "429" in last_error:
                print(f"Model {model_name} rate-limited (429), trying next...")
                continue
            break 
            
    return f"Error: All models failed. Last error: {last_error}", history

def validate_command_wrapper(command):
    return validate_command(command, client, MODELS[0])