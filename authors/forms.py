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
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Password',
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one upper case letter, '
            'one lowercase letter and one number.'
        ),
        validators=[strong_password]
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Repeat your password',
    )

    # essa é outra forma de sobrescrever os elementos do form
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]
        # exclude = ['first_name'] # ao invés de passar os fields pode apenas excluir os que não deseja
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Type your email here',
            'username': 'Type your username',
        }
        help_texts = {
            'email': 'Enter a valid email'
        }
        error_messages = {
            'username': {
                'required': 'This field must not be empty',
                'max_length': 'Este campo deve ter menos de x caracteres.'
            }
        }

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
                'password2': [
                    password_confirmation_error,
                    'Another error'
                ],
            })
        return cleaned_data
