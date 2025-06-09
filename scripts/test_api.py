import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")  # Ensure your .env file contains this

# API Endpoint
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "deepseek/deepseek-r1-distill-llama-70b:free"

# Function to test the API
def test_api():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": "What is the meaning of life?"}]
    }

    print("\n🔍 Sending API request...")

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)

        # Check HTTP status
        if response.status_code != 200:
            print(f"\n❌ API Request Failed ({response.status_code}): {response.text}")
            return
        
        json_response = response.json()
        print("\n✅ API Response:\n", json.dumps(json_response, indent=2))

        # Extract AI message
        ai_message = json_response.get("choices", [{}])[0].get("message", {}).get("content", "No content found")
        print("\n🎯 Extracted Message:\n", ai_message)

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request Error: {e}")

# Run the test
if __name__ == "__main__":
    test_api()
