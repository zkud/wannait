from django.db import models
from django.contrib.auth.models import User


class ProductManager(models.Manager):
    """ Inspired by Django documentation """
    def product_info(self, product_id: int):
        # TODO: change this dump baseline to real connection
        backend_answer = self.model(
            id=product_id,
            name='The best product',
            image_url='none',
            description="".join(['The best description. ' for _ in range(100)])
        )

        return backend_answer

    def for_registered_user(self, user_id):
        # TODO: change this dump baseline to real connection
        backend_answer = [
            self.model(
                id=index, name='name for registered',
                image_url='none')
            for index in range(50)
        ]
        return backend_answer

    def for_anonymous_user(self):
        # TODO: change this dump baseline to real connection
        backend_answer = [
            self.model(
                id=index, name='name for anonymous',
                image_url='none')
            for index in range(50)
        ]
        return backend_answer

    def for_owner(self, user_id):
        # TODO: change this dump baseline to real connection
        backend_answer = [
            self.model(
                id=index, name='name for owner',
                image_url='none')
            for index in range(50)
        ]
        return backend_answer


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1000)
    image_url = models.URLField(max_length=1000)
    description = models.CharField(max_length=10000)
    objects = ProductManager()

    def __str__(self):
        return self.name


class CommentsManager(models.Manager):
    def comments_of_product(self, product_id: int):
        comments_text_variants = (
            'good, good, good, good, good, good, good',
            'bad',
            'awesome and cooo0000000000000000000000000000000000000adjfadjlafk;djflk;dsjflkd;jfads;ladfjl;djs;ladsjl;d\
            jadfkl;ajdl;fkdjfld;skjfadslk;dfsajlk;fdasjldasfjafdls;jfdsjfsdl;dfjl;dsfjsdl;jds\
            jasfdl;kdsjl;kdjla;jdsl;jadfsl;adsjlkdsjlf;dskjadsl;kjfadskl;ajdsal;fds\
            jadsflkjadsl;kajsdldsjl;ooooooooooooooooooooooooool',
            'trash'
        )

        user = User.objects.get(id=2)

        comments = [
            self.model(text=comments_text_variants[index % 4], user=user)
            for index in range(40)
        ]

        return comments


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    objects = CommentsManager()

    def __str__(self):
        return self.user.username + ' : ' + self.text

