from typing import Any, List

from fastapi import APIRouter

from blog.api_crud import category, post
from blog.schemas import (AllPostList, CategoryOut, CreateCategory, CreatePost,
                          PostByCategoryList, SinglePost, UpdateCategory,
                          UpdatePost)

router = APIRouter()


@router.get("/posts/", response_model=List[AllPostList])
def get_multiple_posts(offset: int = 0, limit: int = 10) -> Any:
    """
    Endpoint to get multiple posts based on offset and limit values.
    """
    return post.get_multiple(offset=offset, limit=limit)


@router.post("/posts/", status_code=201, response_model=SinglePost)
def create_post(request: CreatePost) -> Any:
    """
    Endpoint to create single post.
    """
    return post.create(obj_in=request)


@router.post("/tags/", status_code=201, response_model=CategoryOut)
def create_category(request: CreateCategory) -> Any:
    """
    Endpoint to create single category.
    """
    return category.create(obj_in=request)


@router.get("/tags/", response_model=List[CategoryOut])
def get_multiple_categories(offset: int = 0, limit: int = 10) -> Any:
    """
    Get multiple categories.
    """
    query = category.get_multiple(limit=limit, offset=offset)
    return list(query)


@router.get("/posts/{slug}/", response_model=SinglePost)
def get_post(slug: str) -> Any:
    """
    Get single blog post.
    """
    return post.get(slug=slug)


@router.get("/tags/{slug}/", response_model=List[PostByCategoryList])
def get_posts_by_category(slug: str) -> Any:
    """
    Get all posts belonging to a particular category
    """
    query = post.get_posts_by_category(slug=slug)
    return list(query)


@router.put("/posts/{slug}/", response_model=SinglePost)
def update_post(slug: str, request: UpdatePost) -> Any:
    """
    Update a single blog post.
    """
    return post.update(slug=slug, obj_in=request)


@router.put("/tags/{slug}/", response_model=CategoryOut)
def update_category(slug: str, request: UpdateCategory) -> Any:
    """
    Update a single blog category.
    """
    return category.update(slug=slug, obj_in=request)


@router.delete("/posts/{slug}/")
def delete_post(slug: str) -> Any:
    """
    Delete a single blog post.
    """
    return post.delete(slug=slug)


@router.delete("/tags/{slug}/", response_model=CategoryOut)
def delete_category(slug: str) -> Any:
    """
    Delete a single blog category.
    """
    return category.delete(slug=slug)

