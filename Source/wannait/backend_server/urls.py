from django.urls import include, path
from rest_framework import routers


from .views import ProductViewSet
from .views import LikeViewSet
from .views import CommentViewSet
from .views import UserViewSet

from .views import LikeDetail
from .views import CommentDetail
from .views import ProductDetail


app_name = 'backend_server'


router = routers.DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'like', LikeViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'user', UserViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('product/<int:pk>', ProductDetail.as_view()),
    path('like/<int:pk>', LikeDetail.as_view()),
    path('comment/<int:pk>', CommentDetail.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

