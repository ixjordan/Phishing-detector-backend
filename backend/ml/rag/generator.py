import os
import requests
from dotenv import load_dotenv

load_dotenv()


API_URL = "https://router.huggingface.co/v1/chat/completions"
model = "HuggingFaceTB/SmolLM3-3B:hf-inference"


HF_TOKEN = os.getenv("HF_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def generate_explanation(context: dict) -> str:
    """
    Takes in context containing prediction, message, metadata, etc.
    Returns LLM-generated explanation using Hugging Face chat completion.
    """
    prompt = build_prompt(context)

    payload = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "model": model
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    print("[DEBUG] Status:", response.status_code)
    print("[DEBUG] Response:", response.text)

    if response.status_code == 200:
        try:
            raw_text = response.json()["choices"][0]["message"]["content"].strip()
            return extract_json_block(raw_text)
        except (KeyError, IndexError) as e:
            print("[ERROR] Unexpected response structure:", e)
            return "Error: Response format was invalid."
    else:
        print("[ERROR] LLM API failed:", response.status_code, response.text)
        return "Error: Could not generate explanation at this time."

def build_prompt(context: dict) -> str:
    """
    Builds a concise prompt for phishing explanation — returns JSON-ready output.
    """
    msg = context.get("text", "")
    prob = context.get("prediction", {}).get("prob_smishing", 0.0)
    urls = context.get("urls", [])
    numbers = context.get("phone_numbers", [])
    is_valid_number = context.get("enriched_phone_numbers", [])
    is_malicious_url = context.get("enriched_urls", [])

    return f"""
You are an expert security assistant.

A user scanned the following message for phishing risk:

\"{msg}\"

Context:
- Model phishing probability: {round(prob * 100, 2)}%
- Extracted phone numbers: {numbers}
- Extracted URLs: {urls}
- Phone legitimacy check: {is_valid_number}
- URL threat detection: {is_malicious_url}

Your task is to clearly explain why this message might be phishing.

Now return your output in the following JSON format:

{{
  "confidence": "High" | "Medium" | "Low",
  "summary": "Brief summary of why it's suspicious.",
  "reasons": [
    "Reason 1 (max 15 words)",
    "Reason 2 (max 15 words)",
    "Reason 3 (max 15 words)"
  ]
}}

Only return valid JSON. Do not include any additional explanation or internal thoughts. and do not write in first person 
""".strip()



import json
import re

def extract_json_block(text: str) -> dict:
    """
    Extract JSON object from a string containing extra text.
    """
    try:
        json_match = re.search(r"{\s*\"confidence\".*}", text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
    except Exception as e:
        print("[ERROR] Failed to parse JSON block:", e)
    return {"error": "Could not parse explanation JSON."}
