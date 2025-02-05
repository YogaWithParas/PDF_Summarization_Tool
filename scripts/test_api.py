import requests
import json

# API Key & URL
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "deepseek/deepseek-r1-distill-llama-70b:free"

# Function to test the API response
def test_api():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": "Hello, can you respond with a short test message?"}]
    }
    
    print("🔍 Sending API request...")
    
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        print("\n🔹 Status Code:", response.status_code)

        if response.status_code != 200:
            print("❌ API Request Failed:", response.text)
            return
        
        try:
            json_response = response.json()
            print("\n✅ JSON Response:\n", json.dumps(json_response, indent=2))
            print("\n🎯 Extracted Message:\n", json_response["choices"][0]["message"]["content"])
        except json.JSONDecodeError:
            print("\n⚠️ API Response is not JSON. Full response:")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print("\n🚨 Request Exception:", e)

# Run the test
if __name__ == "__main__":
    test_api()
