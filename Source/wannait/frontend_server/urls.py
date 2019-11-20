from django.urls import path
from .views import RecommendationsView
from .views import OwnedProductsView
from .views import ProductInfoView
from .views import AnonymousProductInfoView
from .views import RegisteredProductInfoView
from .views import OwnerProductInfoView

from .views import login_view
from .views import logout_view
from .views import register_view


app_name = 'frontend_server'


urlpatterns = [
    path('', RecommendationsView.as_view(), name='index'),
    path('info/<int:id>', AnonymousProductInfoView.as_view(), name='info'),
    path('accounts/signin/', login_view, name='signin'),
    path('accounts/signup/', register_view, name='signup'),
    path('accounts/signout/', logout_view, name='signout')
]
