from fastapi import APIRouter
from typing import Dict, List
from app.schemas.faqs import FAQ
from app.database.faq_list import faqs

router = APIRouter(prefix="/faqs", tags=["faqs"])

@router.get("/", response_model=Dict[str, List[FAQ]])
async def get_faqs():
    """
    Get frequently asked questions (FAQs) grouped by category.
    """
    grouped_faqs = {}
    for faq in faqs:
        if faq.label not in grouped_faqs:
            grouped_faqs[faq.label] = []
        grouped_faqs[faq.label].append(faq)
    return grouped_faqs 