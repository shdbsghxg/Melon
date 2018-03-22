from django import forms

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
