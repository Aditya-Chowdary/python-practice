# llm_utils.py
import requests
import json
import os # For potentially getting Ollama config from .env
from dotenv import load_dotenv

load_dotenv() # Load .env file

# Ollama API endpoint and model name
# Can be overridden by .env variables OLLAMA_API_URL and OLLAMA_MODEL_NAME
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/chat")
MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME", "mistral") # Ensure this model is pulled via `ollama pull <model_name>`

FABULOUS_SYSTEM_PROMPT = (
    "You are FabuBot, a fantastically organized and cheerful AI assistant. "
    "Your responses should be encouraging, slightly flamboyant, and always helpful. "
    "Keep your responses concise. Sparkle with positivity! When asked to extract information, "
    "strictly follow the JSON format requested."
)

def query_ollama_chat(messages, is_json_mode=False):
    """
    Generic function to query the Ollama chat completions endpoint.
    `messages` should be a list of message objects, e.g.,
    [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
    """
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.7 # Default temperature
        }
    }
    if is_json_mode:
        payload["format"] = "json"
        payload["options"]["temperature"] = 0.1 # Lower temp for deterministic JSON

    try:
        # print(f"DEBUG: Sending to Ollama ({OLLAMA_API_URL}, model: {MODEL_NAME}): {json.dumps(payload, indent=2)}")
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        response.raise_for_status()
        response_data = response.json()
        # print(f"DEBUG: Received from Ollama: {json.dumps(response_data, indent=2)}")
        if "message" in response_data and "content" in response_data["message"]:
            return response_data["message"]["content"]
        elif "error" in response_data:
            print(f"Ollama API Error from model '{MODEL_NAME}': {response_data['error']}")
            return None
        else:
            print(f"Ollama API Error: Unexpected response format from model '{MODEL_NAME}': {response_data}")
            return None
    except requests.exceptions.ConnectionError:
        print(f"Ollama Connection Error: Could not connect to Ollama server at {OLLAMA_API_URL}.")
        print(f"  - Ensure Ollama is installed and the server is active (try 'ollama list' in terminal).")
        print(f"  - Ensure the model '{MODEL_NAME}' is pulled (ollama pull {MODEL_NAME}).")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ollama Request Error: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Ollama API Error: Could not decode JSON from response: {response.text}")
        return None

def extract_reminder_details(user_input: str):
    """
    Uses Ollama to extract task and datetime string from user input.
    """
    prompt_for_extraction = f"""
User's request: "{user_input}"

Your task is to extract the core reminder task and the natural language representation of the date and time for this reminder.
Respond ONLY with a valid JSON object containing "task" and "datetime_str".
The "task" should be a concise description of what to do.
The "datetime_str" should be the part of the user's input that specifies the time or date.
If you cannot determine a specific task or time, return "task": null or "datetime_str": null.

Example 1:
User's request: "Remind me to call Sarah tomorrow at 3 PM"
Your JSON response:
{{
  "task": "call Sarah",
  "datetime_str": "tomorrow at 3 PM"
}}

Example 2:
User's request: "Don't forget the groceries next Friday evening"
Your JSON response:
{{
  "task": "the groceries",
  "datetime_str": "next Friday evening"
}}

Example 3:
User's request: "Tell me a joke"
Your JSON response:
{{
  "task": null,
  "datetime_str": null
}}

Example 4:
User's request: "Book flight for next month"
Your JSON response:
{{
  "task": "Book flight",
  "datetime_str": "next month"
}}

User's request: "{user_input}"
Your JSON response:
"""
    messages = [
        {"role": "system", "content": "You are an expert assistant that extracts specific information from user requests and responds ONLY in valid JSON format as specified."},
        {"role": "user", "content": prompt_for_extraction}
    ]

    llm_response_content = query_ollama_chat(messages, is_json_mode=True)

    if llm_response_content:
        try:
            details = json.loads(llm_response_content)
            return details.get("task"), details.get("datetime_str")
        except json.JSONDecodeError:
            print(f"LLM Error: Could not parse JSON from Ollama response: '{llm_response_content}'")
            json_start = llm_response_content.find('{')
            json_end = llm_response_content.rfind('}') + 1
            if json_start != -1 and json_end != -1 and json_start < json_end:
                json_str = llm_response_content[json_start:json_end]
                try:
                    details = json.loads(json_str)
                    print("LLM Warning: Had to perform fallback JSON extraction.")
                    return details.get("task"), details.get("datetime_str")
                except json.JSONDecodeError:
                    print(f"LLM Error (fallback): Still could not parse JSON from: '{json_str}'")
            return None, None
    else:
        print("LLM Error: No content received from Ollama for extraction.")
        return None, None

def generate_fabulous_response(prompt_text: str):
    """
    Generates a fabulous, friendly response from Ollama.
    """
    messages = [
        {"role": "system", "content": FABULOUS_SYSTEM_PROMPT},
        {"role": "user", "content": prompt_text}
    ]
    response_content = query_ollama_chat(messages)

    if response_content:
        return response_content.strip()
    else:
        return "Oh dear, my local circuits are a bit fizzy right now! Could you try that again, sweetie?"

if __name__ == '__main__':
    print(f"--- Testing LLM Utils (Ollama: {MODEL_NAME} @ {OLLAMA_API_URL}) ---")
    print("\n--- Testing Extraction ---")
    test_task, test_dt_str = extract_reminder_details("Remind me to buy glitter tomorrow morning")
    print(f"Extracted Task: {test_task}, Datetime String: {test_dt_str}")

    test_task, test_dt_str = extract_reminder_details("Get concert tickets for Friday next week")
    print(f"Extracted Task: {test_task}, Datetime String: {test_dt_str}")

    test_task, test_dt_str = extract_reminder_details("What's the weather?")
    print(f"Extracted Task: {test_task}, Datetime String: {test_dt_str}")
    print("\n--- Testing Fabulous Response ---")

    confirmation = generate_fabulous_response("I've just set a reminder for 'buy glitter' for 'tomorrow morning'. Can you confirm this in a fabulous way?")
    print(f"FabuBot Confirmation: {confirmation}")

    greeting = generate_fabulous_response("Greet the user as FabuBot.")
    print(f"FabuBot Greeting: {greeting}")