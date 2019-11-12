from django.db import models


class ProductManager(models.manager):
    """ Inspired by Django documentation """
    def for_registered_user(self, user_id):
        # TODO: change this dump baseline to real connection
        backend_answer = [
            self.model(
                id=index, name='name for registered',
                image_url='images/cat.jpg')
            for index in range(20)
        ]
        return backend_answer

    def for_anonymous_user(self):
        # TODO: change this dump baseline to real connection
        backend_answer = [
            self.model(
                id=index, name='name for registered',
                image_url='images/cat.jpg')
            for index in range(20)
        ]
        return backend_answer

    def for_owner(self, user_id):
        # TODO: change this dump baseline to real connection
        backend_answer = [
            self.model(
                id=index, name='name for owner',
                image_url='images/cat.jpg')
            for index in range(20)
        ]
        return backend_answer


class Product(models.Model):
    id = models.IntegerField()
    name = models.CharField()
    image_url = models.URLField()
    objects = ProductManager()

    def __str__(self):
        return self.name
