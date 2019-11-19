from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic import ListView


from .models import Product


class RecommendationsView(ListView):
    template_name = 'frontend_server/index.html'
    context_object_name = 'products'
    model = Product

    def get_queryset(self):
        user_id = self.request.session.get('user_id')

        # if user logged in
        if user_id is not None:
            return self.model.objects.for_registered_user(user_id)
        else:
            return self.model.objects.for_anonymous_user()


@method_decorator(login_required, name='get')
class OwnedProductsView(ListView):
    template_name = 'frontend_server/owned.html'
    context_object_name = 'products'
    model = Product

    def get_queryset(self):
        owner_id = self.request.session.get('user_id')

        return self.model.objects.for_owner(owner_id)


class ProductInfoView(DetailView):
    model = Product
    context_object_name = 'product'

    def get_object(self, queryset=None):
        product_id: int = self.kwargs['id']

        return self.model.objects.product_info(product_id)


class AnonymousProductInfoView(ProductInfoView):
    template_name = 'frontend_server/product_info.html'


@method_decorator(login_required, name='get')
class RegisteredProductInfoView(ProductInfoView):
    pass


@method_decorator(login_required, name='get')
class OwnerProductInfoView(ProductInfoView):
    pass
