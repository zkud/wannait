from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class BackendProduct(models.Model):
    owner = models.ForeignKey('auth.User', related_name='BackendProduct', on_delete=models.CASCADE, default=0)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1000)
    image_url = models.URLField(max_length=1000)
    description = models.CharField(max_length=10000)

    def __str__(self):
        return self.name


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BackendProduct
        fields = ['name', 'id', 'image_url', 'description']


class BackendComment(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(BackendProduct, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='BackendComment', on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)

    def __str__(self):
        return self.user.username + ' : ' + self.text


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BackendComment
        fields = ['product', 'id', 'text']


class BackendLike(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(BackendProduct, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='BackendLike', on_delete=models.CASCADE)


class LikeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BackendLike
        fields = ['product', 'id']
