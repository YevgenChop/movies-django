from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager


class User(AbstractBaseUser):
    username = None
    email = models.CharField(max_length=255, unique=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return f"{self.username}"
