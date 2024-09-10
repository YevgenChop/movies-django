from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    created_by = models.ForeignKey(
        'authentication.User', on_delete=models.CASCADE)

    genres = models.ManyToManyField('genres.Genre')
    actors = models.ManyToManyField('actors.Actor')

    def __str__(self):
        return self.title
