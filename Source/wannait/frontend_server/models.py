import requests
import json

from random import randint

from django.db import models
from django.contrib.auth.models import User

HOSTS = ['http://127.0.0.1:8000/']


mock_likes = {}


def random_host() -> str:
    return HOSTS[randint(0, len(HOSTS) - 1)]


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1000)
    image_url = models.URLField(max_length=1000)
    description = models.CharField(max_length=10000)

    @staticmethod
    def deserialize(json_dict):
        return Product(
            owner=User.objects.get(id=int(json_dict['owner'])),
            id=int(json_dict['id']),
            name=json_dict['name'],
            image_url=json_dict['image_url'],
            description=json_dict['description']
        )

    @staticmethod
    def deserialize_from_slim(json_dict):
        return Product(
            owner=User.objects.get(id=int(json_dict['owner'])),
            id=int(json_dict['id']),
            name=json_dict['name'],
            image_url=json_dict['image_url']
        )


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)

    @staticmethod
    def deserialize(json_dict, product):
        return Comment(
            user=User.objects.get(id=int(json_dict['owner'])),
            product=product,
            text=json_dict['text']
        )

    def __str__(self):
        return self.user.username + ' : ' + self.text


class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def deserialize(json_list, product):
        if len(json_list) > 0:
            return Like(
                user=User.objects.get(id=int(json_list[0]['owner'])),
                product=product
            )
        else:
            return None


class ProductManager(models.Manager):
    """ Inspired by Django documentation """
    def change_product(self, user_id: int, product_id: int,
                       image_url: str, name: str,
                       description: str):
        url = random_host() + 'backend/crud/products/{}/'.format(product_id)
        product = self.product_info(product_id, user_id)

        if product.owner.id == user_id:
            new_data = {
                'description': description,
                'image_url': image_url,
                'name': name,
                'id': product_id,
                'owner': user_id
            }

            requests.put(url, data=new_data)


    def delete_product(self, user_id: int, product_id: int):
        # get product info & check that user is owner
        url = random_host() + 'backend/crud/products/{}'.format(product_id)
        backend_answer = requests.get(url).json()

        # if product exists and user is owner
        if ('owner' in backend_answer.keys()
                and int(backend_answer['owner']) == user_id):
            requests.delete(url)
            return True
        else:
            return False

    def product_info(self, product_id: int, user_id: int):
        url = random_host() + 'backend/custom/detailedproduct/{}/{}'.format(product_id,
                                                                            user_id)
        backend_answer = requests.get(url).json()

        product = Product.deserialize(backend_answer)
        product.like = Like.deserialize(backend_answer['likes'], product)
        product.comments = [
            Comment.deserialize(json_dict, product)
            for json_dict in backend_answer['comments']
        ]

        return product

    def for_any_user(self, user_id: int, page: int):
        url = random_host() + 'backend/custom/recommendations/{}/{}'.format(user_id, page)
        backend_answer = requests.get(url).json()

        products = [Product.deserialize_from_slim(json_dict)
                    for json_dict in backend_answer]
        likes = [Like.deserialize(json_dict['likes'], product)
                 for json_dict, product in zip(backend_answer, products)]

        def include(product, like):
            product.like = like
            return product
        return [include(product, like)
                for product, like in zip(products, likes)]

    def for_registered_user(self, user_id, page: int):
        return self.for_any_user(user_id, page)

    def for_anonymous_user(self, page: int):
        return self.for_any_user(0, page)

    def for_owner(self, user_id):
        url = random_host() + 'backend/custom/owned/{}'.format(user_id)
        backend_answer = requests.get(url).json()

        products = [Product.deserialize_from_slim(json_dict)
                    for json_dict in backend_answer]

        return products


class LikesManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_like(self, user_id, product_id):
        url = random_host() + 'backend/custom/like/{}/{}'.format(user_id, product_id)
        requests.post(url=url)

    def set_dislike(self, user_id, product_id):
        url = random_host() + 'backend/custom/like/{}/{}'.format(user_id, product_id)
        requests.delete(url=url)


class CommentsManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_comment(self, product_id: int, user_id: int, text: str):
        url = random_host() + 'backend/crud/comments/'

        new_comment = {
            "text": text,
            "owner": user_id,
            "product": product_id
        }

        requests.post(url=url, data=new_comment)


# I LIKE DECENCIES!!!!!!!!!!!!!!!!!!!!!!!
Product.objects = ProductManager()
Like.objects = LikesManager()
Comment.objects = CommentsManager()
