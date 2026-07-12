import os
import sys
import requests
from dotenv import load_dotenv

# Fix windows terminal emoji printing
sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables from backend/.env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def test_llm():
    invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
    stream = False

    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        print("Error: NVIDIA_API_KEY not found in environment variables.")
        return

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "text/event-stream" if stream else "application/json"
    }

    payload = {
        "model": "z-ai/glm-5.2",
        "messages": [{"role": "user", "content": "Hello! Are you responding?"}],
        "max_tokens": 2048,
        "temperature": 0.15,
        "top_p": 1.00,
        "frequency_penalty": 0.00,
        "presence_penalty": 0.00,
        "stream": stream
    }

    try:
        print(f"Sending request to {payload['model']} via NVIDIA API (180s timeout)...")
        # Added timeout=180 as requested
        response = requests.post(invoke_url, headers=headers, json=payload, timeout=180)
        response.raise_for_status()

        if stream:
            for line in response.iter_lines():
                if line:
                    print(line.decode("utf-8"))
        else:
            print("Success! Response received:\n")
            print(response.json()["choices"][0]["message"]["content"])
            
    except requests.exceptions.Timeout:
        print("Error: Request timed out after 180 seconds.")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    test_llm()
