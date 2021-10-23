from datetime import date, datetime
from pathlib import Path
from typing import Any, Callable, List, Union

from django.conf import settings
from django.db import models
from pydantic import AnyUrl

from blog.managers import CategoryManager, PostManager


def upload_image_path(
    instance: Any,
    filename: str) -> Union[str, Callable, Path]:
    """
    Set up the default thumbnail upload path.
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" %(instance.slug, ext)
    return "blog_post_thumbnails/%s/%s" %(instance.slug, filename)


class Category(models.Model):
    """
    Model for blog tags.
    """
    title: str = models.CharField(max_length=200)
    description: str = models.CharField(max_length=200, blank=True, null=True)
    slug: str = models.SlugField(unique=True, blank=True)
    parent: Union[str, int, list] = models.ForeignKey(
        'self', 
        null=True, default=1,
        related_name='tags', 
        on_delete=models.SET_DEFAULT
    )
    active: bool = models.BooleanField(default=False)
    updated: datetime = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_on: datetime = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects: CategoryManager = CategoryManager()

    class Meta:
        constraints: List[Any] = [
            models.UniqueConstraint(
                fields=['title', 'slug'],
                name='unique_blog_category'
            ),
        ]
        verbose_name_plural: str = "categories"
        
    def __repr__(self) -> str:
        return f"<class {self.slug}>"

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    """
    Model for Blog Posts.
    """
    user: Any = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1,
        null=True,
        on_delete=models.SET_DEFAULT,
        related_name="posts"
    )
    category: Any = models.ForeignKey(
        Category,
        null=True, default=1, blank=True,
        on_delete=models.SET_DEFAULT,
        related_name='post_category'
    )
    title: str = models.CharField(max_length=250)
    description: str = models.TextField(null=True, blank=True)
    content: str = models.TextField(default="Create a post.")
    slug: str = models.SlugField(unique=True, blank=True)
    thumbnail: Union[AnyUrl, str] = models.FileField(
        upload_to=upload_image_path, 
        null=True, blank=True, max_length=1000
    )
    draft: bool = models.BooleanField(default=False)
    publish: date = models.DateField(auto_now=False, auto_now_add=False)
    read_time: int = models.IntegerField(default=0)
    view_count:int = models.PositiveIntegerField(default=0)
    updated: datetime = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_on: datetime = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    objects: PostManager = PostManager()
    
    class Meta:
        verbose_name: str = "post"
        verbose_name_plural: str = "posts"
        ordering: list = ["-publish", "title"]

    def __repr__(self) -> str:
        return "<Post %r>" % self.title

    def __str__(self) -> str:
        return f"{self.title}"

    def get_thumbnail_url(self) -> Union[Path, str, AnyUrl]:
        timestamp = "%s%s%s%s%s" % (datetime.now().year, datetime.now().day, datetime.now().hour, datetime.now().minute,
                                    datetime.now().second)
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return "%s?enc=%s" % (self.thumbnail.url, timestamp)
        
        

    

        

# def posts_pre_save_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)

#     if instance.content:
#         html_string = instance.content
#         calc_read_length = get_read_length(html_string)
#         instance.read_length = calc_read_length


# def category_pre_save_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)


# models.signals.pre_save.connect(posts_pre_save_receiver, sender=Post)
# models.signals.pre_save.connect(category_pre_save_receiver, sender=Category)
