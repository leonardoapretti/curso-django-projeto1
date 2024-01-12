from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=65)

    # Define o nome singular e plural que aparecerá na admin do django
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    # Define o nome que aparecerá quando esse model for chamado como string (quando a gente abre as categorias na admin do django é o atributo definido aqui que será exibido)
    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField()
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
    is_published = models.BooleanField(False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/')
    # quando apagar a categoria vinculada altera o valor do campo para null
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Receita'
        verbose_name_plural = 'Receitas'
