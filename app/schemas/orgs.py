from typing import Optional
from pydantic import BaseModel, conint
from datetime import datetime

class OrgCreate(BaseModel):
    name: str
    latitude: float
    longitude: float
    address: str
    contact: str
    image_url: Optional[str] = None 

class OrgResponse(BaseModel):
    id: str
    name: str
    latitude: float
    longitude: float
    address: str
    contact: str
    created_at: datetime
    rating: Optional[int] = None
    image_url: Optional[str] = None 
    
class OrgRating(BaseModel):
    user_id: str
    rating: conint(ge=1, le=5)   # type: ignore
