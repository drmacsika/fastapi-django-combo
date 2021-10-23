from typing import Any, List

from fastapi import APIRouter

from contact.api_crud import contact
from contact.schemas import ContactCreate, ContactOut

router = APIRouter()

@router.post("/", status_code=201, response_model=ContactOut)
async def create_contact(request: ContactCreate) -> Any:
    """
    End point for contact creation.
    This should always be placed above the single GET endpoint.
    """
    return await contact.create(obj_in=request)

