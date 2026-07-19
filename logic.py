import os
from dotenv import load_dotenv
from openai import OpenAI
from security import validate_command

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

MODELS = ["gemini-2.5-flash-lite", "gemini-2.0-flash"]

def get_cli_command(user_text, prompt_version, history):
    """
    sending ChatCompletion request to the LLM with the System prompt and the user input.
    """
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
    return validate_command(command, client)