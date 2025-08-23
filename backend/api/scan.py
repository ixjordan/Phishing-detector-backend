from fastapi import APIRouter, HTTPException, UploadFile, File
import tempfile
import requests
from models.input_models import TextScanRequest
from ocr.tesseract_engine import extract_text
from utils.text_analyser import extract_metadata
from ml.classifier.model import predict
from uuid import uuid4
import os
import json




router = APIRouter(tags=["image_scanner"])

@router.post("/scan-image")
async def scan_image(file: UploadFile = File(...)):
    
    try:
        with tempfile.NamedTemporaryFile("wb", delete=False) as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name
        
        # Extract text from the image
        extracted_text = extract_text(temp_file_path)

        # Extract metadata from the text. send off to be embedded 
        metadata = extract_metadata(extracted_text)

        prediction = predict(metadata["cleaned_text"])
        metadata["prediction"] = prediction

        scan_id = str(uuid4())  # generate a unique scan ID

        # Save full scan result to disk
        os.makedirs("results", exist_ok=True)
        with open(os.path.join("results", f"scan_{scan_id}.json"), "w") as f:
            json.dump(metadata, f, indent=2)


        return{
            "scan_id": scan_id,
            "prediction": prediction,
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@router.post("/scan-text")           
async def scan_text(request: TextScanRequest):

    metadata = extract_metadata(request.text)

    return metadata
    