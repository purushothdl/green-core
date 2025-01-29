from pydantic import BaseModel
from typing import List

class FAQ(BaseModel):
    label: str 
    question: str
    answer: str