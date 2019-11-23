from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views import View

from django.utils.datastructures import MultiValueDictKeyError

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User

from django.http import JsonResponse

from .forms import UserSignupForm
from .forms import UserSigninForm
from .forms import CommentForm
from .forms import DeleteForm
from .forms import LikeForm
from .forms import DislikeForm

from .models import Product
from .models import Comment
from .models import Like


# OK
class RecommendationsView(ListView):
    # TODO: download bootstrap 4
    template_name = 'frontend_server/index.html'
    context_object_name = 'products'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            page = int(self.request.GET['page'])
        except MultiValueDictKeyError:
            page = 1

        if self.request.user.is_authenticated:
            context['products'] = self.model.objects.for_registered_user(self.request.user.id,
                                                                         page)
        else:
            context['products'] = self.model.objects.for_anonymous_user(page)

        context['next_page_number'] = page + 1
        context['next_page_exists'] = len(context['products']) > 35
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        return []


# OK
@method_decorator(login_required, name='post')
class LikeView(View):
    model = Like

    def post(self, request):
        form = LikeForm(request.POST)

        product_id = int(form.data['product_id'])
        user_id = request.user.id

        print('like {} by {}'.format(product_id, user_id))

        self.model.objects.set_like(
            user_id,
            product_id
        )

        return JsonResponse("good", safe=False)


# OK
@method_decorator(login_required, name='post')
class DislikeView(View):
    model = Like

    def post(self, request):
        form = DislikeForm(request.POST)

        product_id = int(form.data['product_id'])
        user_id = request.user.id

        print('dislike {} by {}'.format(product_id, user_id))

        self.model.objects.set_dislike(
            user_id,
            product_id
        )

        return JsonResponse("good", safe=False)


# OK
@method_decorator(login_required, name='post')
class CommentView(View):
    model = Comment

    def post(self, request):
        form = CommentForm(request.POST)

        text = form.data['text']
        product_id = int(form.data['product_id'])
        user_id = request.user.id

        self.model.objects.add_comment(product_id, user_id, text)

        return redirect('../info/{}'.format(product_id))


# OK
@method_decorator(login_required, name='post')
class DeleteProductView(View):
    model = Product

    def post(self, request):
        form = DeleteForm(request.POST)

        product_id = int(form.data['product_id'])
        user_id = request.user.id

        if self.model.objects.delete_product(user_id, product_id):
            return HttpResponseRedirect(
                reverse(
                    'frontend_server:owned'
                )
            )
        else:
            return redirect('../info/{}'.format(product_id))


# OK
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
        owner_id = self.request.user.id

        return self.model.objects.for_owner(owner_id)


# OK
class ProductInfoView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'frontend_server/product_info.html'

    def get_context_data(self, **kwargs):
        product_id: int = self.kwargs['id']
        user = self.request.user
        user_id = user.id if user.is_authenticated else 0

        context = super().get_context_data(**kwargs)

        context['product'] = Product.objects.product_info(product_id, user_id)
        context['comments'] = context['product'].comments
        context['user'] = user
        context['user_is_owner'] = context['product'].owner.id == user_id
        context['like'] = context['product'].like
        context['comment_form'] = CommentForm()

        return context

    def get_object(self, queryset=None):
        product_id: int = self.kwargs['id']
        user = self.request.user
        user_id = user.id if user.is_authenticated else 0

        return Product.objects.product_info(product_id, user_id)


# OK
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


# OK
def register_view(request):
    next = request.GET.get('next')
    form = UserSignupForm(request.POST or None)
    context = {}

    if form.is_valid():
        username = form.cleaned_data.get('login')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email1')

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


# OK
@login_required
def logout_view(request):
    logout(request)
    return redirect('/')
