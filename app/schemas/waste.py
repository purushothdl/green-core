from enum import Enum
from pydantic import BaseModel
from datetime import datetime

class WasteType(str, Enum):
    RECYCLABLE = "Recyclable"
    BIODEGRADABLE = "Biodegradable"
    HAZARDOUS = "Hazardous"

class WasteDisposalCreate(BaseModel):
    org_name: str
    waste_type: WasteType  
    weight: float
    photo_url: str

class WasteDisposalResponse(BaseModel):
    id: str
    user_id: str
    org_name: str
    waste_type: WasteType  
    weight: float
    photo_url: str
    date: datetime