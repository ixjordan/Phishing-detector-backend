from fastapi import APIRouter, HTTPException, UploadFile, File
import tempfile
import requests
import json 
import os
from Ml.rag.generator import generate_explanation


router = APIRouter(tags=["rag-explainer"])

@router.post("/explain/{scan_id}")
def generate_reasoning(scan_id: str):
    """
    """
    print("[DEBUG] Current working directory:", os.getcwd())
    results = {}
    try:
        # access previosuly loaded scan results
        path = os.path.join("results", f"scan_{scan_id}.json")
        with open (path, "r") as file:
            scan_results = json.load(file)
        
        # return the json outputted by the rag 
        explanation = generate_explanation(scan_results)
        reasons = explanation.get("reasons", [])

        results = {
            "scan_id": scan_id,
            "Confidence": explanation.get('confidence', 'uknown'),
            "summary": explanation.get("summary", ""),
            "reasons": reasons

         }
        return results

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Scan results for {scan_id} not found. ")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while generating reasoning: {str(e)}")
    