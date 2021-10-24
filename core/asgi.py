import os
from importlib.util import find_spec

from django.apps import apps
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles

# Export Django settings env variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
apps.populate(settings.INSTALLED_APPS)

# This endpoint imports should be placed below the settings env declaration
# Otherwise, django will throw a configure() settings error
from core.api_router import router as api_router

# Get the Django WSGI application we are working with
application = get_wsgi_application()

# This can be done without the function, but making it functional
# tidies the entire code and encourages modularity
def get_application() -> FastAPI:
    # Main Fast API application
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        debug=settings.DEBUG
    )
    
    # Set all CORS enabled origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.ALLOWED_HOSTS] or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include all api endpoints
    app.include_router(api_router, prefix=settings.API_V1_STR) 
    
    # Mounts an independent web URL for Django WSGI application
    app.mount(f"{settings.WSGI_APP_URL}", WSGIMiddleware(application))
    
    # Mounts an independent web URL for DRF API
    app.mount(f"{settings.DRF_V1_STR}", WSGIMiddleware(application))
    
    # Set Up the static files and directory to serve django static files
    app.mount("/static", StaticFiles(directory="static"), name="static")  
    return app


app = get_application()
