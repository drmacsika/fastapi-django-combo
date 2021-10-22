from typing import Generic, List, Optional, Type, TypeVar
from unicodedata import category

from core.base_crud import SLUGTYPE, BaseCRUD
from core.utils import unique_slug_generator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model, Prefetch, query
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from blog.models import Category, Post
from blog.schemas import CreateCategory, CreatePost, UpdateCategory, UpdatePost


class PostCRUD(BaseCRUD[Post, CreatePost, UpdatePost, SLUGTYPE]):
    """
    CRUD Operation for blog posts
    """
    
    def get(self, slug: SLUGTYPE) -> Optional[Post]:
        """
        Get single blog post.
        """
        try:
            query = Post.objects.select_related("user", "category").get(slug=slug)
            return query
        except ObjectDoesNotExist:
            raise HTTPException(status_code=404, detail="This post does not exists.")
        
    def get_multiple(self, limit:int = 100, offset: int = 0) -> List[Post]:
        """
        Get multiple posts using a query limit and offset flag.
        """
        query = Post.objects.select_related("user", "category").all()[offset:offset+limit]
        if not query:
            raise HTTPException(status_code=404, detail="There are no posts.")
        return list(query)
    
    def get_posts_by_category(self, slug: SLUGTYPE) -> List[Post]:
        """
        Get all posts belonging to a particular category.
        """
        query_category = Category.objects.filter(slug=slug)
        if not query_category:
            raise HTTPException(status_code=404, detail="This category does not exist.")
        query = Post.objects.filter(category__slug=slug).select_related("user").all()
        return list(query)
    
    def create(self, obj_in: CreatePost) -> Post:
        """
        Create an post.
        """
        slug = unique_slug_generator(obj_in.title)
        post = Post.objects.filter(slug=slug)
        if not post:
            slug = unique_slug_generator(obj_in.title, new_slug=True)
        obj_in = jsonable_encoder(obj_in)
        query = Post.objects.create(**obj_in)
        return query
        
    def update(self, obj_in: UpdatePost, slug: SLUGTYPE) -> Post:
        """
        Update an item.
        """
        self.get(slug=slug)
        if not isinstance(obj_in, list):
            obj_in = jsonable_encoder(obj_in)
        return Post.objects.filter(slug=slug).update(**obj_in)
    
    def delete(self, slug: SLUGTYPE) -> Post:
        """Delete an item."""
        self.model.objects.filter(slug=slug).delete()
        return {"detail": "Successfully deleted!"}


class CategoryCRUD(BaseCRUD[Category, CreateCategory, UpdateCategory, SLUGTYPE]):
    """
    CRUD Operation for blog categories.
    """
    
    def get(self, slug: SLUGTYPE) -> Optional[Category]:
        """
        Get a single category.
        """    
        try:
            query = Category.objects.get(slug=slug)
            return query
        except ObjectDoesNotExist:
            raise HTTPException(status_code=404, detail="This post does not exists.")
        
    def get_multiple(self, limit:int = 100, offset: int = 0) -> List[Category]:
        """
        Get multiple categories using a query limiting flag.
        """
        query = Category.objects.all()[offset:offset+limit]
        if not query:
            raise HTTPException(status_code=404, detail="There are no posts.")
        return list(query)

    def create(self, obj_in: CreateCategory) -> Category:
        """
        Create a category.
        """
        slug = unique_slug_generator(obj_in.title)
        category = Category.objects.filter(slug=slug)
        if category:
            raise HTTPException(status_code=404, detail="Category exists already.")
        obj_in = jsonable_encoder(obj_in)
        query = Category.objects.create(**obj_in)
        return query
        
    def update(self, obj_in: UpdateCategory, slug: SLUGTYPE) -> Category:
        """
        Update a category.
        """
        if not isinstance(obj_in, list):
            obj_in = jsonable_encoder(obj_in)
        return self.model.objects.filter(slug=slug).update(**obj_in)
    
    def delete(self, slug: SLUGTYPE) -> Post:
        """Delete a category."""
        Post.objects.filter(slug=slug).delete()
        return {"detail": "Successfully deleted!"}


post = PostCRUD(Post)
category = CategoryCRUD(Category)
