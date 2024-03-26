from collections import defaultdict

from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr
from django.core.exceptions import ValidationError
from utils.string import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # o default_dict ja atribui um valor no momento em que uma chave é criada. No caso abaixo ele cria uma lista para cada chave criada, o que evita a utilização de ifs para verificação se há ou não listas
        # é uma boa prática capturar todos os erros do formulário e lançá-los de uma vez ao enviar o form
        self._my_erros = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', 'preparation_time_unit', 'servings', 'servings_unit', 'preparation_steps', 'cover', 'category',
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                    ('Litros', 'Litros'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            )
        }

    # no método clean é possível validar TODOS os campos do formulário, contudo, pode ficar confuso.
    # é bom quando tem que validar campos que dependem um do outro
    # se for utilizar os métodos cleans separados tem que utilizar o clean geral para lançar os ValidationErrors
    # ou valida em um método ou no outro, se colocar nos dois ele captura apenas o erro lançado no ultimo método clean
    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if len(title) < 5:
            self._my_erros['title'].append('Must have at least 5 chars.')

        if title == description:
            self._my_erros['title'].append('Cannot be equal to description.')
            self._my_erros['description'].append('Cannot be equal to title.')

        if self._my_erros:
            raise ValidationError(self._my_erros)

        return super_clean

    # no método clean_field_name voce valida campo a campo, e a forma de recuperar os cleaned_data também é diferente

    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.cleaned_data.get(field_name)
        if not is_positive_number(field_value):
            self._my_erros[field_name].append(
                'Must be a positive number.')
        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.cleaned_data.get(field_name)
        if not is_positive_number(field_value):
            self._my_erros[field_name].append('Must be a positive number.')
        return field_value

    def clean_category(self):
        field_name = 'category'
        field_value = self.cleaned_data.get(field_name)
        if field_value is None:
            self._my_erros[field_name].append('Category must not be empty.')
