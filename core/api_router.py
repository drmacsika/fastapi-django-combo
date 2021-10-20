from blog.endpoints import router as blog_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(blog_router, prefix="/blog", tags=["Blog"])
