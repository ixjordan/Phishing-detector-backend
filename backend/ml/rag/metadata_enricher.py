import re 
from typing import List, Dict, Any
import requests
from dotenv import load_dotenv
import os

load_dotenv()


def is_scam_number(number: str, country_code: str) -> list:
    """Check if a phone number is a known scam number.
    This function can be extended to include more sophisticated checks.
    Args:
        number (str): The phone number to check.
        country_code (str): The country code for the phone number.
    Returns: 
    """
    number_data = {}


    url = os.getenv("NUM_VERIFY_URL")
    access_key = os.getenv("NUM_VERIFY_ACCESS_KEY")
    params = {
        "access_key": access_key,
        "number": number,
        "country_code": country_code  # Assuming UK numbers, adjust as necessary
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        print("[DEBUG] Scam number check response:", data)
        return data.get("valid", False) and data.get("scam", False)
    else:        
        print("[ERROR] Failed to check scam number:", response.status_code, response.text)
        return None  # or handle the error as needed




def is_safe_url(extracted_url: str) -> bool:
    """
    Check if a URL is safe using Google Safe Browsing API.
    Args:
        url (str): The URL to check.
    Returns:"""
    url = os.getenv("SAFE_BROWSING_URL")

    API_KEY = os.getenv("SAFE_BRWOSING_API_KEY")

    # request body
    payload = {
        "client": {
            "clientId": "phishing-detector-app",
            "clientVersion": "1.5.2"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": extracted_url}]
        }
    }

    # hit api endpoint
    response = requests.post(
        f"{url}?key={API_KEY}",
        json=payload
    )
    # if hit is successful
    if response.status_code == 200:
        data = response.json()
        # return enriched url data
        return {
            "url":extracted_url,
            "malicious": bool(data.get("matches")),
            "matches": data.get("matches", [])
        }
    else:
        print("[ERROR] Failed to check URL safety:", response.status_code, response.text)
        return {"url": url, "error": response.text}



def enrich_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enrich metadata with additional information.
    This function can be extended to include more checks and enrichments.
    """
    # enrich eahc number extracted from text
    enriched_numbers = []
    for number in metadata.get("phone_numbers", []):
        is_valid = is_scam_number(number, 'GB')
        enriched_numbers.append({
            "number": number,
            "is_scam": is_valid
        })

    # enrich each url extracted
    enriched_urls = []
    for url in metadata.get("urls", []):
        result = is_safe_url(url)
        enriched_urls.append(result)


    metadata["enriched_phone_numbers"] = enriched_numbers
    metadata["enriched_urls"] = enriched_urls

    return metadata


if __name__ == "__main__":
    # Example usage
    # sample_metadata = {
    #     "phone_number": "07826514174",
    #     "url": "https://example.com"
    # }
    
    # print(is_scam_number(sample_metadata["phone_number"], 'GB'))

    test_url = "https://gov.engdwpah.top/uk"  # Replace with your test URL
    result = is_safe_url(test_url)
    print("Result:", result)

    # enriched_metadata = enrich_metadata(sample_metadata)
    # print(enriched_metadata)
    # # This will print the enriched metadata with additional checks