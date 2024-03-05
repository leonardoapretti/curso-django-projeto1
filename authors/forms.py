from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


class RegisterForm(forms.ModelForm):
    # aqui nós não sobrescrevemos e sim adicionamos os campos diretamente nos elementos do form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex: John')
        add_placeholder(self.fields['last_name'], 'Ex: Smith')

    # essa é uma forma de sobrescrever os atributos dos elementos do form. é recomendado fazer assim do que fazer na class Meta
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Type your password here'
        }),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one upper case letter, '
            'one lowercase letter and one number.'
        )
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'repeat your password'
        }),
        label='Repeat your password'
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
            'username': 'Type your username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Type your email here',
            'password': 'Type your password here',
        }
        help_texts = {
            'email': 'Enter a valid email'
        }
        error_messages = {
            'username': {
                'required': 'Esse campo é obrigatório, preencha novamente.',
                'max_length': 'Este campo deve ter menos de x caracteres.'
            }
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your first name here'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Type your last name here'
            }),
        }

    # validação utilizando o método clean_field_name(self)
    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'atenção' in data:
            raise ValidationError(
                'Não digite %(value)s no campo password',
                code='invalid',
                params={'value': 'atenção'}
            )
        return data

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')

        if 'John Doe' in data:
            raise ValidationError(
                'Não digite %(value)s no campo first name',
                code='invalid',
                params={'value': 'John Doe'}
            )
        return data
