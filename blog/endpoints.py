from typing import List

from fastapi import APIRouter

from blog import models, schemas

blog_router = APIRouter()


@blog_router.post("/posts", response_model=schemas.Post)
def create_post(post: schemas.PostCreate):
    post = models.Post.objects.create(**post.dict())

    return post


blog_router.get("/posts", response_model=List[schemas.Post])
def read_posts():
    posts = list(models.Post.objects.all())

    return posts
