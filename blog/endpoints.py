from typing import List

from fastapi import APIRouter

from blog import models, schemas

api_router = APIRouter()


@api_router.post("/posts", response_model=schemas.Post)
def create_post(post: schemas.PostCreate):
    post = models.Post.objects.create(**post.dict())

    return post


@api_router.get("/posts", response_model=List[schemas.Post])
def read_posts():
    posts = list(models.Post.objects.all())

    return posts
