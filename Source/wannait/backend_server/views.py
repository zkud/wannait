from rest_framework import viewsets
from rest_framework import views
from rest_framework import generics
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
                                   product_objects=None,
                                   retrieve_comments=True, retrieve_likes=True):
    # retrieve product data & serialize it
    if product_objects is None:
        product_objects = BackendProduct.objects.all()
        products = product_objects.filter(id=product_id)
    else:
        products = [*filter(lambda product: product.id == product_id, product_objects)]
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


class LikeView(generics.CreateAPIView, generics.DestroyAPIView):
    def post(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        product_id = self.kwargs['product_id']

        like_doesnt_exists = len(BackendLike.objects.filter(owner=user_id,
                                                            product=product_id)) == 0

        if like_doesnt_exists:
            owner = User.objects.get(id=user_id)
            product = BackendProduct.objects.get(id=product_id)
            BackendLike(owner=owner, product=product).save()
        return Response('success')

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        product_id = self.kwargs['product_id']
        BackendLike.objects.filter(owner=user_id, product=product_id).delete()
        return Response('success')



class RecommendationsView(views.APIView):
    PAGE_SIZE = 35

    def get(self, *args, **kwargs):
        # TODO: refactor queries in loop
        user_id = self.kwargs['user_id']
        page = self.kwargs['page_number']

        algorithm = RecommendationsSearchAlgorithmFactory().spawn(user_id)
        recommendation = algorithm.find_recommendation()[(page - 1)*self.PAGE_SIZE: (page)*self.PAGE_SIZE + 1]

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

