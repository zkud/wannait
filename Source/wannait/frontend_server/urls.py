from django.urls import path
from .views import RecommendationsView
from .views import LikeView
from .views import CommentView
from .views import DislikeView
from .views import OwnedProductsView
from .views import ProductInfoView

from .views import login_view
from .views import logout_view
from .views import register_view


app_name = 'frontend_server'


urlpatterns = [
    path('', RecommendationsView.as_view(), name='index'),
    path('owned', OwnedProductsView.as_view(), name='owned'),
    path('info/<int:id>', ProductInfoView.as_view(), name='info'),
    path('like/<int:id>', LikeView.as_view(), name='like'),
    path('dislike/<int:id>', DislikeView.as_view(), name='dislike'),
    path('comment/', CommentView.as_view(), name='comment'),
    path('accounts/signin/', login_view, name='signin'),
    path('accounts/signup/', register_view, name='signup'),
    path('accounts/signout/', logout_view, name='signout')
]
