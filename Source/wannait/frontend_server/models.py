from django.db import models
from django.contrib.auth.models import User


mock_likes = {}
mock_comments = {}


class ProductManager(models.Manager):
    """ Inspired by Django documentation """
    def product_info(self, product_id: int):
        # TODO: change this dump baseline to real connection
        backend_answer = self.model(
            id=product_id,
            name='The best product',
            image_url='none',
            description="".join(['The best description. ' for _ in range(100)])
        )

        return backend_answer

    def for_registered_user(self, user_id):
        # TODO: change this dump baseline to real connection
        backend_answer = [
            self.model(
                id=index, name='name for registered',
                image_url='none')
            for index in range(50)
        ]
        return backend_answer

    def for_anonymous_user(self):
        # TODO: change this dump baseline to real connection
        backend_answer = [
            self.model(
                id=index, name='name for anonymous',
                image_url='none')
            for index in range(50)
        ]
        return backend_answer


    def for_owner(self, user_id):
        # TODO: change this dump baseline to real connection
        backend_answer = [
            self.model(
                id=index, name='name for owner',
                image_url='none')
            for index in range(50)
        ]
        return backend_answer


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1000)
    image_url = models.URLField(max_length=1000)
    description = models.CharField(max_length=10000)
    objects = ProductManager()

    def __str__(self):
        return self.name


class CommentsManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_comment(self, product_id: int, user_id: int, text: str):
        new_comment = self.model(text=text, user=User.objects.get(id=user_id))

        if product_id in mock_comments.keys():
            mock_comments[product_id] += [new_comment]
        else:
            mock_comments[product_id] = [new_comment]

    def comments_of_product(self, product_id: int):
        if product_id in mock_comments.keys():
            return mock_comments[product_id]
        else:
            return []


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    objects = CommentsManager()

    def __str__(self):
        return self.user.username + ' : ' + self.text


class LikesManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_like(self, user_id, product_id):
        if user_id in mock_likes.keys():
            mock_likes['user_id'] += [product_id]
        else:
            mock_likes['user_id'] = [product_id]

    def set_dislike(self, user_id, product_id):
        if user_id in mock_likes.keys():
            mock_likes['user_id'].remove(product_id)
        else:
            mock_likes['user_id'] = [product_id]

    def user_likes(self, user_id):
        if user_id in mock_likes.keys():
            return mock_likes['user_id']
        else:
            return []


class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = LikesManager()
