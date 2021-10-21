from typing import Generic, List, Optional, Type, TypeVar

from django.db.models import Model
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=Model)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)
SLUGTYPE = TypeVar("SLUGTYPE", "int", "str")


class BaseCRUD(Generic[ModelType, CreateSchema, UpdateSchema, SLUGTYPE]):
    """
    Base class for all crud operations
    Methods to Create, Read, Update, Delete (CRUD).
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get(self, slug: SLUGTYPE) -> Optional[ModelType]:
        """
        Get single item.
        """
        return self.model.objects.get(slug=slug)
    
    def get_multiple(self, limit:int = 100, offset:int = 0) -> List[ModelType]:
        """
        get multiple items using a query limiting flag.
        """
        return self.model.objects.all()[offset:offset+limit]
    
    def create(self, obj_in: CreateSchema) -> ModelType:
        """
        Create an item.
        """
        if not isinstance(obj_in, list):
            obj_in = jsonable_encoder(obj_in)
        return self.model.objects.create(**obj_in)
        
    def update(self, obj_in: UpdateSchema, slug: SLUGTYPE) -> ModelType:
        """
        Update an item.
        """
        if not isinstance(obj_in, list):
            obj_in = jsonable_encoder(obj_in)
        return self.model.objects.filter(slug=slug).update(**obj_in)
    
    def delete(self, slug: SLUGTYPE) -> ModelType:
        """Delete an item."""
        self.model.objects.filter(slug=slug).delete()
        return {"detail": "Successfully deleted!"}
