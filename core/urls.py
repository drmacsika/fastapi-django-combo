from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles import views
from django.urls import path

urlpatterns = [path("admin/", admin.site.urls)]
