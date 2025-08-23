import os
import requests
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.1"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def generate_explanation(prompt: str) -> str:
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.9
        }
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    data = response.json()

    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"]
    else:
        return "[Error] No generated output from model."
