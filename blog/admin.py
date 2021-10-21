from django.contrib import admin

from blog.models import Category, Post


class BlogCategoryAdmin(admin.ModelAdmin):
    list_display: list = ['title', 'active']
    list_display_links: list = ['title']
    list_filter: list = ['updated', 'active']
    search_fields: list = ['title']
    list_editable: list = ['active']
    list_per_page: list = 10
    ordering: tuple = ('-id',)


admin.site.register(Category, BlogCategoryAdmin)


class PostModelAdmin(admin.ModelAdmin):
    list_display: list = ['title', 'updated', 'created_on', 'publish', 'draft']
    list_display_links: list = ['title']
    list_filter: list = ['updated', 'created_on', 'publish']
    list_editable: list = ['draft']
    search_fields: list = ['title', 'content']
    list_per_page: int = 10
    ordering: tuple = ('-id',)

    class Meta:
        model: Post = Post

admin.site.register(Post, PostModelAdmin)
