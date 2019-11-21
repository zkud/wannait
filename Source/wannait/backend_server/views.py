from rest_framework import viewsets
from rest_framework import generics
from django.contrib.auth.models import User


from .models import BackendProduct
from .models import BackendLike
from .models import BackendComment


from .models import ProductSerializer
from .models import LikeSerializer
from .models import CommentSerializer
from .models import UserSerializer


class ProductDetail(generics.RetrieveUpdateAPIView):
    queryset = BackendProduct.objects.all()
    serializer_class = ProductSerializer


class LikeDetail(generics.RetrieveUpdateAPIView):
    queryset = BackendLike.objects.all()
    serializer_class = LikeSerializer


class CommentDetail(generics.RetrieveUpdateAPIView):
    queryset = BackendComment.objects.all()
    serializer_class = CommentSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
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

