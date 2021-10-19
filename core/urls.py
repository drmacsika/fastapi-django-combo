from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles import views
from django.urls import path

urlpatterns = [path("admin/", admin.site.urls)]


# if settings.DEBUG:
#     from django.urls import re_path

#     urlpatterns += [re_path(r"^static/(?P<path>.*)$", views.serve)]




# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
