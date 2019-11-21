from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class BackendProduct(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=2)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1000)
    image_url = models.URLField(max_length=1000)
    description = models.CharField(max_length=10000)

    def __str__(self):
        return self.name


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = BackendProduct
        fields = ['owner', 'name', 'id', 'image_url', 'description']


class BackendComment(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(BackendProduct, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=2)
    text = models.CharField(max_length=1000)

    def __str__(self):
        return self.user.username + ' : ' + self.text


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = BackendComment
        fields = ['user', 'product', 'id', 'text']


class BackendLike(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(BackendProduct, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=2)


class LikeSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = BackendLike
        fields = ['user', 'product', 'id']
