from rest_framework import viewsets
from rest_framework import views
from rest_framework.response import Response
from django.contrib.auth.models import User


from .models import BackendProduct
from .models import BackendLike
from .models import BackendComment


from .models import ProductSerializer
from .models import SlimProductSerializer
from .models import LikeSerializer
from .models import CommentSerializer
from .models import UserSerializer


from .models import RecommendationsSearchAlgorithm
from .models import RecommendationsSearchAlgorithmFactory


def retrieve_detailed_product_data(product_id:int, user_id:int,
                                   product_serializer=ProductSerializer,
                                   product_objects=BackendProduct.objects.all(),
                                   retrieve_comments=True, retrieve_likes=True):
    # retrieve product data & serialize it
    products = product_objects.filter(id=product_id)
    if len(products) == 0:
        return {}
    product = products[0]
    product_serializer = product_serializer(data=products, many=True)
    # thanks to django rest framework for this crutch
    product_serializer.is_valid()
    result = product_serializer.data[0]

    # do the same with comments and likes
    if retrieve_comments:
        comments = BackendComment.objects.filter(product=product)
        comment_serializer = CommentSerializer(data=comments, many=True)
        comment_serializer.is_valid()
        result['comments'] = comment_serializer.data

    if retrieve_likes:
        likes = BackendLike.objects.filter(product=product, owner=user_id)
        like_serializer = LikeSerializer(data=likes, many=True)
        like_serializer.is_valid()
        result['likes'] = like_serializer.data

    return result


class RecommendationsView(views.APIView):
    def get(self, *args, **kwargs):
        # TODO: refactor queries in loop
        user_id = self.kwargs['user_id']

        algorithm = RecommendationsSearchAlgorithmFactory().spawn(user_id)
        recommendation = algorithm.find_recommendation()

        result = []
        for product in recommendation:
            result.append(
                retrieve_detailed_product_data(
                    product.id, user_id,
                    product_objects=recommendation,
                    product_serializer=SlimProductSerializer,
                    retrieve_comments=False
                )
            )

        return Response(result)


class OwnedProductsView(viewsets.ReadOnlyModelViewSet):
    serializer_class = SlimProductSerializer

    def get_queryset(self):
        return BackendProduct.objects.filter(owner=self.kwargs['user_id'])


class DetailedProductView(views.APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            retrieve_detailed_product_data(
                self.kwargs['product_id'],
                self.kwargs['user_id']
            )
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = BackendProduct.objects.all()
    serializer_class = ProductSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = BackendLike.objects.all()
    serializer_class = LikeSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = BackendComment.objects.all()
    serializer_class = CommentSerializer

