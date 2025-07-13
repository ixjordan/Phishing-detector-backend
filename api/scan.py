from fastapi import APIRouter, HTTPException, UploadFile, File
import tempfile
import requests
from models.input_models import TextScanRequest
from ocr.tesseract_engine import extract_text
from utils.text_analyser import extract_metadata


router = APIRouter(tags=["image_scanner"])

@router.post("/scan-image")
async def scan_image(file: UploadFile = File(...)):
    
    try:
        with tempfile.NamedTemporaryFile("wb", delete=False) as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name
        
        # Extract text from the image
        extracted_text = extract_text(temp_file_path)

        # Extract metadata from the text
        metadata = extract_metadata(extracted_text)

        # For now, we will return the extracted text directly
        return metadata
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@router.post("/scan-text")           
async def scan_text(request: TextScanRequest):

    metadata = extract_metadata(request.text)

    return metadata
    