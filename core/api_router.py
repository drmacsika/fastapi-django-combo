from blog.endpoints import router as blog_router
from fastapi import APIRouter

api_router = APIRouter()
api_router.add_router(blog_router, prefix="/blog", tags=["Blog"])
