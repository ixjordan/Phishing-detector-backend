import pytesseract
import cv2
import numpy as np

def preprocess_image(image_path):
    """
    image_path: str
        Path to the image file to be preprocessed.
    """
    
    try:
        # Read the image
        image = cv2.imread(image_path)
        # Check if the image was loaded successfully
        if image is None:
            raise ValueError("Image not found or unable to read.")
        
        # Convert to grayscale, resize, apply thresholding and median blur
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        gray = cv2.medianBlur(gray, 3)

        # Return the preprocessed image
        return gray
    # Handle exceptions for image processing
    except Exception as e:
        raise RuntimeError(f"Error in preprocessing image: {e}")

def extract_text(image_path):
    """
    Extract text from an image using Tesseract OCR
    image_path: str
        Path to the image file from which text is to be extracted.
    """

    try:
        # Preprocess the image
        preprocess_imaged_image = preprocess_image(image_path)
        # Use Tesseract to extract text
        text = pytesseract.image_to_string(preprocess_imaged_image, lang='eng')
        # Strip any leading/trailing whitespace from the extracted text
        return text.strip()
    # Handle exceptions for text extraction
    except Exception as e:
        raise RuntimeError(f"Error in extracting text: {e}")
    

if __name__ == "__main__":
    # Example usage
    image_path = input("Enter the path to the image file: ")
    try:
        extracted_text = extract_text(image_path)
        print("Extracted Text:", extracted_text)
    except RuntimeError as e:
        print(e)