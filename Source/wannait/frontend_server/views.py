from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic import ListView


from django.shortcuts import render, redirect


from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User


from .forms import UserSignupForm
from .forms import UserSigninForm
from .models import Product
from .models import Comment


class RecommendationsView(ListView):
    # TODO: download bootstrap 4
    template_name = 'frontend_server/index.html'
    context_object_name = 'products'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = self.request.user

        return context

    def get_queryset(self):
        # if user logged in
        if self.request.user.is_authenticated:
            return self.model.objects.for_registered_user(self.request.user.id)
        else:
            return self.model.objects.for_anonymous_user()


@method_decorator(login_required, name='get')
class OwnedProductsView(ListView):
    template_name = 'frontend_server/owned.html'
    context_object_name = 'products'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = self.request.user

        return context

    def get_queryset(self):
        owner_id = self.request.session.get('user_id')

        return self.model.objects.for_owner(owner_id)


class ProductInfoView(DetailView):
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        product_id: int = self.kwargs['id']

        context = super().get_context_data(**kwargs)

        context['comments'] = Comment.objects.comments_of_product(product_id)

        return context

    def get_object(self, queryset=None):
        product_id: int = self.kwargs['id']

        return self.model.objects.product_info(product_id)


class AnonymousProductInfoView(ProductInfoView):
    template_name = 'frontend_server/product_info.html'


@method_decorator(login_required, name='get')
class RegisteredProductInfoView(ProductInfoView):
    template_name = 'frontend_server/registered_product_info.html'


@method_decorator(login_required, name='get')
class OwnerProductInfoView(ProductInfoView):
    template_name = 'frontend_server/owner_product_info.html'


def login_view(request):
    next = request.GET.get('next')
    form = UserSigninForm(request.POST or None)
    context = {}

    if form.is_valid():
        username = form.cleaned_data.get('login')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        login(request, user)

        if next:
            return redirect(next)
        return redirect('/')
    else:
        try:
            context['form_error'] = "\n".join(form.errors['__all__'])
        except:
            pass

    context['form'] = form

    return render(request, "frontend_server/signin.html", context)


def register_view(request):
    next = request.GET.get('next')
    form = UserSignupForm(request.POST or None)
    context = {}

    if form.is_valid():
        username = form.cleaned_data.get('login')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email1')

        print('here new')
        user = User.objects.create_user(username, email, password)
        login(request, user)

        if next:
            return redirect(next)
        return redirect('/')
    else:
        try:
            context['form_error'] = "\n".join(form.errors['__all__'])
        except:
            pass

    context['form'] = form

    return render(request, "frontend_server/signup.html", context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')
