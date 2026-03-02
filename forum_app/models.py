from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=255, blank=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
