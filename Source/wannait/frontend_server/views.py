from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import ListView


from .models import Product


class RecommendationsView(ListView):
    template_name = 'frontend_server/index.hmtl'
    context_object_name = 'recommendations'
    model = Product


class OwnedProductsView(ListView):
    template_name = 'frontend_server/owner.html'
    context_object_name = 'owned_product'
    model = Product


class ProductInfoView(DetailView):
    pass


class AnonymousProductInfoView(ProductInfoView):
    pass


class RegisteredProductInfoView(ProductInfoView):
    pass


class OwnerProductInfoView(ProductInfoView):
    pass
