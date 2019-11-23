from django.urls import include, path
from rest_framework import routers


from .views import ProductViewSet
from .views import LikeViewSet
from .views import CommentViewSet
from .views import UserViewSet
from .views import RecommendationsView
from .views import OwnedProductsView


app_name = 'backend_server'


router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'users', UserViewSet)


urlpatterns = [
    path('crud/', include(router.urls)),
    path('custom/recommendations/<int:user_id>', RecommendationsView.as_view({'get': 'list'})),
    path('custom/owned/<int:user_id>', OwnedProductsView.as_view({'get': 'list'})),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

