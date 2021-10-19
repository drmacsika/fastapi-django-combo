import os

from django.apps import apps
from django.conf import settings
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
apps.populate(settings.INSTALLED_APPS)


from blog.endpoints import blog_router
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from starlette.middleware.cors import CORSMiddleware

application = get_wsgi_application()


def get_application() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(blog_router, prefix=settings.API_V1_STR, tags=["Blog"]) 
    app.mount("/web", WSGIMiddleware(application))
    return app


app = get_application()
