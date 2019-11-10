from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import ListView


class RecommendationsView(ListView):
    pass


class OwnedProductsView(ListView):
    pass


class ProductInfoView(DetailView):
    pass


class AnonymousProductInfoView(ProductInfoView):
    pass


class RegisteredProductInfoView(ProductInfoView):
    pass


class OwnerProductInfoView(ProductInfoView):
    pass
