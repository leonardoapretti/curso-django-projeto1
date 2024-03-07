from django import forms
from utils.django_forms import add_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add_placeholder(self.fields['username'], 'Ex: John')
        # add_placeholder(self.fields['password'], 'Type here your password')

    username = forms.CharField(
        label='Type your username',
        widget=forms.TextInput(
            attrs={'placeholder': 'Ex: John'}
        ),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Type here your password'}),
    )
