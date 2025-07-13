from pydantic import BaseModel, model_validator
from typing import Optional

class textScanRequest(BaseModel):
    text: str
    

    @model_validator(mode='before')
    def validate_text(cls, values):
        if not values.get('text'):
            raise ValueError("Text field cannot be empty")
        return values