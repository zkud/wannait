from rest_framework import viewsets
from rest_framework import generics
from django.contrib.auth.models import User


from .models import BackendProduct
from .models import BackendLike
from .models import BackendComment


from .models import ProductSerializer
from .models import SlimProductSerializer
from .models import LikeSerializer
from .models import CommentSerializer
from .models import UserSerializer


class RecommendationsView(viewsets.ReadOnlyModelViewSet):
    serializer_class = SlimProductSerializer

    def get_queryset(self):
        pass


class OwnedProductsView(viewsets.ReadOnlyModelViewSet):
    serializer_class = SlimProductSerializer

    def get_queryset(self):
        return BackendProduct.objects.filter(owner=self.kwargs['user_id'])


class DetailedProductView(generics.RetrieveAPIView):
    serializer_class = FatProductSerializer
    queryset = BackendProduct.objects.all()


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

