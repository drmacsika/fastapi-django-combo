import os

from blog.endpoints import blog_router
from django.apps import apps
from django.conf import settings
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
apps.populate(settings.INSTALLED_APPS)
application = get_asgi_application()


def get_application() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Make a generic api versioning 
    app.include_router(blog_router, prefix="/api") 
    app.mount("/django", WSGIMiddleware(application))
    return app


app = get_application()
