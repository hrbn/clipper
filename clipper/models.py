from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager


from django.db import models


class User(AbstractUser):
    pass


class Clip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clip_user")
    title = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True)
    content = models.TextField(blank=True)
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title
