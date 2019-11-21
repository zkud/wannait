from django.urls import include, path
from rest_framework import routers


from .views import ProductViewSet
from .views import LikeViewSet
from .views import CommentViewSet


app_name = 'backend_server'


router = routers.DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'like', LikeViewSet)
router.register(r'comment', CommentViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls))
]

