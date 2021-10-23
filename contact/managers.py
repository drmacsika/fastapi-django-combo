from django.db import models


class ContactManager(models.Manager):
    def all(self):
        return self.get_queryset()

    def active(self, *args, **kwargs):
        return super(ContactManager, self).filter(active=True)
