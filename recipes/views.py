from django.shortcuts import render
from utils.recipes.factory import make_recipe
from recipes.models import Recipe


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipes/pages/home.html', context=context)


def category(request, category_id):
    recipes = Recipe.objects.filter(
        category__id=category_id, is_published=True).order_by('-id')
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipes/pages/category.html', context=context)


def recipe(request, id_recipe):
    # recipe = Recipe.objects.filter(id=id_recipe)
    recipe = make_recipe()
    context = {
        'recipe': recipe,
        'is_detail_page': True,
        'request': request,
    }
    return render(request, 'recipes/pages/recipe_view.html', context)
