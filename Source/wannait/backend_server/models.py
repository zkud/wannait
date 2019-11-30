from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers
from random import randint


from .ml import FactorizationModel


class BackendProduct(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=2)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    image_url = models.URLField(max_length=1000)
    description = models.CharField(max_length=10000)

    def __str__(self):
        return "Backend Product: \n id={} \n name={}".format(self.id, self.name)


class BackendComment(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(BackendProduct, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=2)
    text = models.CharField(max_length=1000)

    def __str__(self):
        return self.user.username + ' : ' + self.text


class BackendVisit(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(BackendProduct, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=2)


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


class VisitSerializer(serializers.HyperlinkedModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=BackendProduct.objects.all())
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = BackendVisit
        fields = ['owner', 'product', 'id']


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
    PAGE_SIZE = 35

    def find_recommendation(self, page):
        raise NotImplemented


class TopRatingsAlgorithm(RecommendationsSearchAlgorithm):
    PAGE_SIZE = 35

    def find_recommendation(self, page):
        return BackendProduct.objects.annotate(
            num_likes=models.Count('backendlike')
        ).order_by('-num_likes')[(page - 1)*self.PAGE_SIZE: page*self.PAGE_SIZE + 4]


class FactorizationAlgorithm(RecommendationsSearchAlgorithm):
    PAGE_SIZE = 35

    def __init__(self, user_id: int):
        self.user_id = user_id

    def can_find_recommendations(self) -> bool:
        return FactorizationModel.get_instance().user_is_here(self.user_id)

    def find_recommendation(self, page):
        # find the best recommendations
        recommendation = FactorizationModel.get_instance().recommendation_indexes(self.user_id)
        indexes = recommendation[(page - 1)*self.PAGE_SIZE: page*self.PAGE_SIZE + 4]
        result = [BackendProduct.objects.get(id=index) for index in indexes]

        # solve cold start problem
        n_products = BackendProduct.objects.all().count()

        if len(result) > 10:
            random_count = len(result) // 5
            for count in range(random_count):
                random_index = randint(0, n_products // 3)
                random_product = BackendProduct.objects.all().order_by('-id')[random_index]
                result[randint(5, len(result) - 1)] = random_product

        return result


class RecommendationsSearchAlgorithmFactory:
    def spawn(self, user_id: int) -> RecommendationsSearchAlgorithm:
        factorization_algorithm = FactorizationAlgorithm(user_id)

        if factorization_algorithm.can_find_recommendations():
            print('FACTORIZATION')
            return factorization_algorithm
        else:
            print('TOP RATINGS')
            return TopRatingsAlgorithm()

