from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    role = models.CharField(max_length=50, default="customer")
    avatar = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username or self.email

