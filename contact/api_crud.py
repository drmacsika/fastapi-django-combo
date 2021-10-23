from typing import List, Optional, Union

from core.base_crud import SLUGTYPE, BaseCRUD
from core.utils import unique_slug_generator
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from contact.models import Contact
from contact.schemas import ContactCreate


class ContactCRUD(BaseCRUD[Contact, ContactCreate, ContactCreate, SLUGTYPE]):
    
    def create(self, obj_in: ContactCreate) -> Contact:
        obj_in = jsonable_encoder(obj_in)
        query = Category.objects.create(**obj_in)
        return query
    
contact = ContactCRUD(Contact)
