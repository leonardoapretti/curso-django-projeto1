from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
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
            'username': 'Digite seu usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'Digite seu email',
            'password': 'Digite sua senha',
        }
        help_texts = {
            'email': 'Digite um email válido'
        }
        error_messages = {
            'username': {
                'required': 'Esse campo é obrigatório, preencha novamente.',
                'max_length': 'Este campo deve ter menos de x caracteres.'
            }
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Digite seu nome aqui'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Digite seu sobrenome aqui'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Digite sua senha aqui'
            })
        }
