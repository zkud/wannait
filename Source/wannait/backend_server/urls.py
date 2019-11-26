from django.urls import include, path
from rest_framework import routers


from .views import ProductViewSet
from .views import LikeViewSet
from .views import CommentViewSet
from .views import UserViewSet
from .views import VisitViewSet


from .views import RecommendationsView
from .views import OwnedProductsView
from .views import DetailedProductView
from .views import LikeView
from .views import StartRetrainDaemon
from .views import VisitView


app_name = 'backend_server'


router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'users', UserViewSet)
router.register(r'visits', VisitViewSet)


urlpatterns = [
    path('crud/', include(router.urls)),
    path('custom/recommendations/<int:user_id>/<int:page_number>', RecommendationsView.as_view()),
    path('custom/detailedproduct/<int:product_id>/<int:user_id>/', DetailedProductView.as_view()),
    path('custom/owned/<int:user_id>', OwnedProductsView.as_view({'get': 'list'})),
    path('custom/like/<int:user_id>/<int:product_id>', LikeView.as_view()),
    path('custom/visit/<int:user_id>/<int:product_id>', VisitView.as_view()),
    path('custom/start', StartRetrainDaemon.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

