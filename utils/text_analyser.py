import re


def extract_metadata(text: str) -> dict:
    """
    Extract metadata from the given text.
    
    Args:
        text (str): The input text from which to extract metadata.
    
    Returns:
        dict: A dictionary containing extracted metadata such as phone number, email, and cleaned text.
    """
    metadata = {
        "phone_numbers":[],
        "emails": [],
        "urls": [],
        "text": text.strip(),
        "cleaned_text": ""
    }
    
    # For now, we will just return a cleaned version of the text
    cleaned_text = re.sub(r'\s+', ' ', text.strip().lower())

    # regex formats
    uk_phone_regex = r"\+44\s?\d{4}[\s\n]?\d{6}|\(?07\d{3}\)?[\s\n]?\d{3}[\s\n]?\d{3}"
    email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    url_regex = r"\b(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?\b"



    # search text for variables below
    emails = re.findall(email_regex, cleaned_text)
    phone_numbers = re.findall(uk_phone_regex, cleaned_text)
    urls = re.findall(url_regex, cleaned_text)

    email_domains = {e.split('@')[1] for e in emails}
    urls = [u for u in urls if u not in email_domains]

    # Update metadata with extracted information
    metadata["phone_numbers"] = list(set(phone_numbers))
    metadata["emails"] = list(set(emails))
    metadata["urls"] = list(set(urls))
    metadata["cleaned_text"] = cleaned_text


    print("[DEBUG] Extracted metadata:", metadata)

    return metadata

if __name__ == "__main__":
    # Example usage
    sample_text = "jordancroft95@gmail.com +44 7766 948477 07826514174 https://wa.me/447428048446"
   
    metadata = extract_metadata(sample_text)
    print(metadata["phonenumbers"])
    # This will print the cleaned text and any extracted metadata
    # Note: The actual metadata extraction logic is not implemented yet.