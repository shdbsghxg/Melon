from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

__all__ = (
    'SignupForm',
)


class SignupForm(forms.Form):
    username = forms.CharField(
        label='ID',
    )
    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput,
    )
    password_confirm = forms.CharField(
        label='password_confirm',
        widget=forms.PasswordInput,
    )

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise ValidationError('username already exists')
        return data

    def clean_password_confirm(self):
        data = self.cleaned_data['password']
        data2 = self.cleaned_data['password_confirm']
        if data != data2:
            raise ValidationError('password confirmation failed')
        return data
