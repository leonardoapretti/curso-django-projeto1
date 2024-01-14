from django.shortcuts import render
from utils.recipes.factory import make_recipe
from recipes.models import Recipe
from django.shortcuts import get_object_or_404


def home(request):
    recipes = Recipe.objects.all().order_by('-id')
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipes/pages/home.html', context=context)


def category(request, category_id):
    recipes = Recipe.objects.filter(category__id=category_id).order_by('-id')
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipes/pages/home.html', context=context)


def recipe(request, id_recipe):
    context = {
        'recipe': get_object_or_404(Recipe, id_recipe == id),
        'is_detail_page': True,
        'request': request
    }
    return render(request, 'recipes/pages/recipe_view.html', context)
