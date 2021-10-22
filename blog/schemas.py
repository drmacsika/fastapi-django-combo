from datetime import date, datetime
from typing import Any, Generic, List, Optional, Type, Union

from accounts.schemas import UserOut
from pydantic import BaseModel, validator

from blog.models import Category


def confirm_title(value: str) -> str:
    """
    Validation to prevent empty title field.
    Called by the helper function below;
    """
    if not value:
        raise ValueError("Please provide a title.")
    return value

def confirm_slug(value: str) -> str:
    """
    Validation to prevent empty slug field.
    Called by the helperfunction below;
    """
    if not value:
        raise ValueError("Slug cannot be empty.")
    return value


class CategoryBase(BaseModel):
    """
    Base fields for blog post category.
    """
    title: str
    description: Optional[str] = None
    
    _confirm_title = validator("title", allow_reuse=True)(confirm_title)
        
    
class CreateCategory(CategoryBase):
    """
    Fields for creating blog post category.
    """
    ...
    
class UpdateCategory(CategoryBase):
    """
    Fields for updating blog post category.
    """
    # slug: str
    active: bool
    
    # _confirm_slug = validator("slug", allow_reuse=True)(confirm_slug)

    
class CategoryOut(CategoryBase):
    """
    Response for blog post category.
    """    
    slug: str
    active: bool
    
    class Config:
        orm_mode = True
        

class CategoryListOut(BaseModel):
    """
    Response for list all categories.
    We made a custom since we need just these two fields.
    """    
    title: str
    slug: str
    
    class Config:
        orm_mode = True
    

class PostBase(BaseModel):
    """Base fields for blog posts."""
    user: UserOut
    title: str
    
    # Validation for title and slug
    _check_title = validator("title", allow_reuse=True)(confirm_title)
    
    # @validator("title")
    # def check_title_availability(cls, value):
    #     if not value:
    #         raise ValueError("Title cannot be empty.")

class CreatePost(PostBase):
    """
    Fields for creating blog post.
    """
    ...
    
    
class UpdatePost(PostBase):
    """
    Fields for updating blog post.
    """
    # slug: Optional[str] = None
    view_count: int
    active: bool
    # updated: datetime
    
    # _check_slug = validator("slug", allow_reuse=True)(confirm_slug)


class SinglePost(PostBase):
    """
    Response for blog post.
    """
    id: int
    slug: str
    view_count: int
    draft: bool = False
    publish: date
    description: Optional[str] = None
    content: Optional[str] = ...
    read_time: int
    category: CategoryOut
    
    class Config:
        orm_mode = True


class AllPostList(PostBase):
    """
    Response for listing all blog posts.
    Custom for just these few fields
    """
    id: int    
    slug: str
    draft: bool = False
    category: CategoryListOut

    class Config:
        orm_mode = True
    
    
class PostByCategoryList(PostBase):
    """
    Response for listing all blog posts.
    Custom for just these few fields.
    """
    id: int    
    slug: str
    draft: bool = False

    class Config:
        orm_mode = True
