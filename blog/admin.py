from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class Postadmin(admin.ModelAdmin):
    list_display = ("id", "title")
