import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://router.huggingface.co/v1/chat/completions"
MODEL_ID = "HuggingFaceTB/SmolLM3-3B:hf-inference"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# Construct chat-style payload
payload = {
    "model": MODEL_ID,
    "messages": [
        {"role": "system", "content": "You are a helpful AI security assistant helping users understand why a message may be phishing."},
        {"role": "user", "content": "Explain why the following message might be a phishing scam: 'Royal Mail: Pay £1.99 to release your parcel: http://bit.ly/xyz'"}
    ],
    "temperature": 0.7,
    "max_tokens": 256
}

print("[DEBUG] Sending request to:", API_URL)
response = requests.post(API_URL, headers=HEADERS, json=payload)

print("[DEBUG] Status:", response.status_code)
print("[DEBUG] Response:", response.json())
