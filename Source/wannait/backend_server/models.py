from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers


class BackendProduct(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=2)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    image_url = models.URLField(max_length=1000)
    description = models.CharField(max_length=10000)

    def __str__(self):
        return self.name


class BackendComment(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(BackendProduct, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=2)
    text = models.CharField(max_length=1000)

    def __str__(self):
        return self.user.username + ' : ' + self.text


class BackendLike(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(BackendProduct, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=2)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=BackendProduct.objects.all())
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = BackendComment
        fields = ['owner', 'product', 'id', 'text']


class LikeSerializer(serializers.HyperlinkedModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=BackendProduct.objects.all())
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = BackendLike
        fields = ['owner', 'product', 'id']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = BackendProduct
        fields = ['owner', 'name', 'id', 'image_url',
                  'description', 'owner']


class SlimProductSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = BackendProduct
        fields = ['name', 'id', 'image_url', 'owner']


class RecommendationsSearchAlgorithm:
    def find_recommendation(self):
        raise NotImplemented


class TopRaitingsAlgorithm(RecommendationsSearchAlgorithm):
    def find_recommendation(self):
        return BackendProduct.objects.all()


class RecommendationsSearchAlgorithmFactory:
    def spawn(self, user_id: int) -> RecommendationsSearchAlgorithm:
        return TopRaitingsAlgorithm()

