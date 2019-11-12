from django.db import models


class Product(models.Model):
    name = models.CharField()
    image_url = models.URLField()

    def __str__(self):
        return self.name
