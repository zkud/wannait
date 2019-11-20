from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views import View


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

from .models import Product
from .models import Comment
from .models import Like


class RecommendationsView(ListView):
    # TODO: download bootstrap 4
    template_name = 'frontend_server/index.html'
    context_object_name = 'products'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = self.request.user

        if self.request.user.is_authenticated:
            context['likes'] = Like.objects.user_likes(self.request.user.id)
        else:
            context['likes'] = []

        return context

    def get_queryset(self):
        # if user logged in
        if self.request.user.is_authenticated:
            return self.model.objects.for_registered_user(self.request.user.id)
        else:
            return self.model.objects.for_anonymous_user()


@method_decorator(login_required, name='post')
class LikeView(View):
    model = Like

    def post(self, request):
        self.model.objects.set_like(
            self.request.user.id,
            self.kwargs['id']
        )

        return JsonResponse("good")


@method_decorator(login_required, name='post')
class DislikeView(View):
    model = Like

    def post(self, request):
        self.model.objects.set_dislike(
            self.request.user.id,
            self.kwargs['id']
        )

        return JsonResponse('good')


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


class ProductInfoView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'frontend_server/product_info.html'

    def get_context_data(self, **kwargs):
        product_id: int = self.kwargs['id']

        context = super().get_context_data(**kwargs)

        context['comments'] = Comment.objects.comments_of_product(product_id)

        context['user'] = self.request.user
        if self.request.user.is_authenticated:
            context['user_is_owner'] = Product.objects.is_owner(self.request.user.id, product_id)
        else:
            context['user_is_owner'] = False
        context['comment_form'] = CommentForm()

        return context

    def get_object(self, queryset=None):
        product_id: int = self.kwargs['id']

        return self.model.objects.product_info(product_id)


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
