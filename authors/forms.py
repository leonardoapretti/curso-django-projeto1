from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
            code='invalid'
        )


class RegisterForm(forms.ModelForm):
    # aqui nós não sobrescrevemos e sim adicionamos os campos diretamente nos elementos do form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], 'Ex: John')
        add_placeholder(self.fields['last_name'], 'Ex: Smith')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['password'], 'Type your password')
        add_placeholder(self.fields['password2'], 'Repeat your password')
    # essa é uma forma de sobrescrever os atributos dos elementos do form. é recomendado fazer assim do que fazer na class Meta
    username = forms.CharField(
        label='Type your username',
        help_text=(
            'Username must have letters, numbers or one of those @ . + - _'
            'The length should be between 4 and 150 characters.'
        ),
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have at least 4 characters.',
            'max_length': 'Username must not be more than 150 characters.'
        },
        min_length=4,
        max_length=150,
    )
    first_name = forms.CharField(
        label='First Name',
        error_messages={'required': 'Write your first name'},
    )
    last_name = forms.CharField(
        label='Last Name',
        error_messages={'required': 'Write your last name'},
    )
    email = forms.EmailField(
        label='Type your email here',
        widget=forms.EmailInput(),
        help_text='Enter a valid email',
        error_messages={'required': 'E-mail must not be empty'},
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one upper case letter, '
            'one lowercase letter and one number.'
        ),
        validators=[strong_password],
    )
    password2 = forms.CharField(
        label='Confirm your password',
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Confirm your password must not be empty'
        },
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Passwords must be equal',
                code='invalid'
            )

            raise ValidationError({
                'password': password_confirmation_error,
                'password2': password_confirmation_error,
            })
        return cleaned_data
