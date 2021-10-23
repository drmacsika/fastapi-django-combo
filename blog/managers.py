from datetime import timezone

from django.db import models


class PostQuerySet(models.query.QuerySet):
    def active(self, *args, **kwargs):
        return super(PostQuerySet, self).filter(draft=False).filter(
            publish__lte=timezone.now())

    def search(self, query):
        lookups = (models.Q(title__icontains=query) |
                   models.Q(content__icontains=query) |
                   models.Q(user__full_name__icontains=query)
                   )
        return self.filter(lookups).distinct()


class CategoryManager(models.Manager):
    def all(self):
        return self.get_queryset()

    def active(self, *args, **kwargs):
        return super(CategoryManager, self).filter(active=True)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset()

    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(
            publish__lte=timezone.now())

    def full_search(self, query):
        return self.get_queryset().search(query)

    def filtered_search(self, query):
        return self.get_queryset().active().search(query)
