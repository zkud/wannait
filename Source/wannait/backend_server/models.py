from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              default=User.objects.get_by_natural_key('ls'))
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1000)
    image_url = models.URLField(max_length=1000)
    description = models.CharField(max_length=10000)

    def __str__(self):
        return self.name


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['owner', 'name', 'id', 'image_url', 'description']


class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)

    def __str__(self):
        return self.user.username + ' : ' + self.text


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['product', 'user', 'id', 'text']


class Like(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class LikeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Like
        fields = ['product', 'user', 'id']
