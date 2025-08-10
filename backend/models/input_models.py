from pydantic import BaseModel, Field
from typing import Optional

class TextScanRequest(BaseModel):
    text: str = Field(...,min_length=1, description="Text to be scanned for metadata extraction.")