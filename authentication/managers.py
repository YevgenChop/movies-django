from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given username must be set')

        with transaction.atomic():
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        return self.create_user(email, password, **extra_fields)
