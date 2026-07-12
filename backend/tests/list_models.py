import os
import requests
from dotenv import load_dotenv

# Load environment variables from backend/.env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def list_models():
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        print("Error: NVIDIA_API_KEY not found in environment variables.")
        return

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }

    print("Fetching available models from NVIDIA API...")
    response = requests.get("https://integrate.api.nvidia.com/v1/models", headers=headers)
    
    if response.status_code == 200:
        models = response.json().get("data", [])
        print(f"\nFound {len(models)} models:")
        for model in models:
            print(f"- {model.get('id')}")
    else:
        print(f"Failed to fetch models. Status Code: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    list_models()
