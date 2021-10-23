from datetime import datetime

from django.db import models

from contact.managers import ContactManager


class Contact(models.Model):
    """
    Models for contacts.
    """
    firstname: str = models.CharField(max_length=100)
    lastname: str = models.CharField(max_length=100)
    email: str = models.EmailField(max_length=255)
    subject: str = models.CharField(max_length=255)
    message: str = models.TextField(max_length=2000)
    active: bool = models.BooleanField(default=False)
    created: datetime = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    objects = ContactManager()
    
    class Meta:
        ordering=["-created"]
    
    def __str__(self) -> str:
        return f"{self.email}"

