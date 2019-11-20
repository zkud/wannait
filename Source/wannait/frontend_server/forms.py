from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class CommentForm(forms.Form):
    product_id = forms.IntegerField(label='')
    text = forms.CharField(widget=forms.Textarea, label='', max_length=1000)


class UserSigninForm(forms.Form):
    # TODO: update forms mockups
    login = forms.CharField(label='Login', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    def clean(self, *args, **kwargs):
        login = self.cleaned_data.get('login')
        password = self.cleaned_data.get('password')

        if login and password:
            user = authenticate(username=login, password=password)

            if not user:
                raise forms.ValidationError('This user does not exist or password is not correct')

            if not user.is_active:
                raise forms.ValidationError('This user is banned')

        return super(UserSigninForm, self).clean(*args, **kwargs)


class UserSignupForm(forms.ModelForm):
    login = forms.CharField(label='Login', max_length=100)
    email1 = forms.EmailField(label='Email', max_length=200)
    email2 = forms.EmailField(label='Confirm email', max_length=200)
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Password'
    )

    class Meta:
        model = User
        fields = [
            'login',
            'email1',
            'email2',
            'password'
        ]

    def clean(self, *args, **kwargs):
        login = self.cleaned_data.get('login')
        email1 = self.cleaned_data.get('email1')
        email2 = self.cleaned_data.get('email2')

        if email1 != email2:
            raise forms.ValidationError("Emails must match")

        email_qs = User.objects.filter(email=email1)

        if email_qs.exists():
            raise forms.ValidationError(
                "This email has already been registered"
            )

        login_qs = User.objects.filter(username=login)

        if login_qs.exists():
            raise forms.ValidationError(
                "This login has already been registered"
            )

        return super(UserSignupForm, self).clean(*args, **kwargs)
