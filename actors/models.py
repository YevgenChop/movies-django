from django.db import models


class Actor(models.Model):
    name = models.CharField(max_length=100)

    created_by = models.ForeignKey(
        'authentication.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
