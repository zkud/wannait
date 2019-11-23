import requests
import json

from random import randint

from django.db import models
from django.contrib.auth.models import User

HOSTS = ['http://127.0.0.1:8000/']


mock_likes = {}


def random_host() -> str:
    return HOSTS[randint(0, len(HOSTS) - 1)]


class ProductManager(models.Manager):
    """ Inspired by Django documentation """

    def delete_product(self, user_id: int, product_id: int):
        return True

    def is_owner(self, user_id: int, product_id: int) -> bool:
        user = User.objects.get(id=user_id)

        backend_answer = requests.get(random_host() + 'backend/product/')

        products = [self.model.deserialize(product)
                    for product in json.loads(backend_answer.text)]

        return user == list(filter(lambda product: product.id == product_id, products))[0].owner

    def product_info(self, product_id: int):
        backend_answer = requests.get(random_host() + 'backend/product/')

        products = [self.model.deserialize(product)
                    for product in json.loads(backend_answer.text)]

        backend_answer = list(filter(lambda product: product.id == product_id, products))[0]

        return backend_answer

    def for_registered_user(self, user_id):
        backend_answer = requests.get(random_host() + 'backend/product/')

        return [self.model.deserialize(product)
                for product in json.loads(backend_answer.text)]

    def for_anonymous_user(self):
        backend_answer = requests.get(url=(random_host() + 'backend/product/'))

        return [self.model.deserialize(product)
                for product in json.loads(backend_answer.text)]

    def for_owner(self, user_id):
        user = User.objects.get(id=user_id)

        backend_answer = requests.get(random_host() + 'backend/product/')

        products = [self.model.deserialize(product)
                    for product in json.loads(backend_answer.text)]

        backend_answer = list(
            filter(lambda product: product.owner == user, products)
        )

        return backend_answer


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1000)
    image_url = models.URLField(max_length=1000)
    description = models.CharField(max_length=10000)
    objects = ProductManager()

    @staticmethod
    def deserialize(json_dict):
        return Product(
            owner=User.objects.get(id=int(json_dict['owner'])),
            id=int(json_dict['id']),
            name=json_dict['name'],
            image_url=json_dict['image_url'],
            description=json_dict['description']
        )

    def __str__(self):
        return self.name


class CommentsManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_comment(self, product_id: int, user_id: int, text: str):
        backend_answer = requests.get(random_host() + 'backend/comment/')
        new_id = int(max(json.loads(backend_answer.text), key=lambda x: int(x['id']))['id']) + 1

        new_comment = {
            "text": text,
            "owner": user_id,
            "product": product_id,
            "id": new_id
        }

        requests.post(url=(random_host() + 'backend/comment/'),
                      data=json.dumps(new_comment))

    def comments_of_product(self, product_id: int):
        backend_answer = requests.get(random_host() + 'backend/comment/')
        product = Product.objects.product_info(product_id)

        comments = filter(
            lambda x: str(x['product']) == str(product_id),
            json.loads(backend_answer.text)
        )

        comments = [self.model.deserialize(dct, product) for dct in comments]

        print('comments {}'.format(json.loads(backend_answer.text)))

        return comments


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    objects = CommentsManager()

    @staticmethod
    def deserialize(json_dict, product):
        return Comment(
            user=User.objects.get(id=int(json_dict['owner'])),
            product=product,
            text=json_dict['text']
        )

    def __str__(self):
        return self.user.username + ' : ' + self.text


class LikesManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_like(self, user_id, product_id):
        print("mock_likes: {}".format(mock_likes))
        if user_id in mock_likes.keys():
            mock_likes[user_id] += [product_id]
        else:
            mock_likes[user_id] = [product_id]

    def set_dislike(self, user_id, product_id):
        print("mock_likes: {}".format(mock_likes))
        if user_id in mock_likes.keys():
            mock_likes[user_id].remove(product_id)
        else:
            mock_likes[user_id] = [product_id]

    def user_likes(self, user_id):
        print("mock_likes: {}".format(mock_likes))
        if user_id in mock_likes.keys():
            return mock_likes[user_id]
        else:
            return []


class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = LikesManager()
