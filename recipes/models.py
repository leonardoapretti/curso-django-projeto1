from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils.crypto import get_random_string


class Category(models.Model):
    name = models.CharField(max_length=65)

    # Define o nome singular e plural que aparecerá na admin do django
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    # Define o nome que aparecerá quando esse model for chamado como string (quando a gente abre as categorias na admin do django é o atributo definido aqui que será exibido)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipes:category', args=(self.id,))


class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    # adiciona essa data no momento de criação do objeto
    created_at = models.DateTimeField(auto_now_add=True)
    # adiciona essa data no momento de atualização do objeto
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(
        default=False, verbose_name='Está publicado?')
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d/', null=True, blank=True, default=None)
    # quando apagar a categoria vinculada altera o valor do campo para null
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Receita'
        verbose_name_plural = 'Receitas'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:recipe', args=(self.id,))

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            exist_slug = Recipe.objects.filter(slug=slug).first()
            if exist_slug is not None:
                slug += get_random_string(length=4)
            self.slug = slug

        return super().save(*args, **kwargs)
