from typing import Generic, List, Optional, Type, TypeVar

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
    
#     >>> voted_choices = Choice.objects.filter(votes__gt=0)
# >>> voted_choices
# <QuerySet [<Choice: The sky>]>
# >>> prefetch = Prefetch('choice_set', queryset=voted_choices)
# >>> Question.objects.prefetch_related(prefetch).get().choice_set.all()
# <QuerySet [<Choice: The sky>]>


# prefetch = Prefetch('choice_set', queryset=voted_choices, to_attr='voted_choices')
# >>> Question.objects.prefetch_related(prefetch).get().voted_choices
# [<Choice: The sky>]
# >>> Question.objects.prefetch_related(prefetch).get().choice_set.all()
    
    
    
    def get(self, slug: SLUGTYPE) -> Optional[Post]:
        """
        Get single blog post.
        """
        user_query = Post.objects.select_related("user").filter(slug=slug)
        prefetch = Prefetch("category", queryset=user_query)
        query = Post.objects.prefetch_related(prefetch).all()
        return query
        
    
    def get_multiple(self, limit=100, offset=0) -> List[Post]:
        """
        get multiple items using a query limiting flag.
        """
        user_query = Post.objects.select_related("user")
        prefetch = Prefetch("category", queryset=user_query)
        query = Post.objects.prefetch_related(prefetch).all()
        return list(query)
    
    def create(self, obj_in: CreatePost) -> Post:
        """
        Create an item.
        """
        slug = unique_slug_generator(obj_in.title)
        post = self.get(slug=slug)
        if post:
            slug = unique_slug_generator(obj_in.title, new_slug=True)
        obj_in = jsonable_encoder(obj_in)
        query = Post.objects.create(**obj_in)
        return query
        
    # def update(self, obj_in: UpdateSchema, slug: SLUGTYPE) -> ModelType:
    #     """
    #     Update an item.
    #     """
    #     if not isinstance(obj_in, list):
    #         obj_in = jsonable_encoder(obj_in)
    #     return self.model.objects.filter(slug=slug).update(**obj_in)
    
    # def delete(self, slug: SLUGTYPE) -> ModelType:
    #     """Delete an item."""
    #     self.model.objects.filter(slug=slug).delete()
    #     return {"detail": "Successfully deleted!"}




class CategoryCRUD(BaseCRUD[Category, CreateCategory, UpdateCategory, SLUGTYPE]):
    """
    CRUD Operation for blog categories.
    """


    def get(self, slug: SLUGTYPE) -> Optional[Category]:
        """
        Get single blogcCategory.
        """
        query = Category.objects.filter(slug=slug).all()
        return query
        
    
    def get_multiple(self, limit=100, offset=0) -> List[Category]:
        """
        get multiple items using a query limiting flag.
        """
        posts = super().get_multiple(limit=limit, offset=offset)
        return list(posts)
    
    
    def create(self, obj_in: CreateCategory) -> Category:
        """
        Create an item.
        """
        slug = unique_slug_generator(obj_in.title)
        category = self.get(slug=slug)
        if category:
            raise HTTPException(status_code=404, detail="Category exists already.")
        obj_in = jsonable_encoder(obj_in)
        query = Category.objects.create(**obj_in)
        return query
        
    # def update(self, obj_in: UpdateSchema, slug: SLUGTYPE) -> ModelType:
    #     """
    #     Update an item.
    #     """
    #     if not isinstance(obj_in, list):
    #         obj_in = jsonable_encoder(obj_in)
    #     return self.model.objects.filter(slug=slug).update(**obj_in)
    
    # def delete(self, slug: SLUGTYPE) -> ModelType:
    #     """Delete an item."""
    #     self.model.objects.filter(slug=slug).delete()
    #     return {"detail": "Successfully deleted!"}


post = PostCRUD(Post)
category = CategoryCRUD(Category)
