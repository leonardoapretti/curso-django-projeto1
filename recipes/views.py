from django.shortcuts import render, get_list_or_404, get_object_or_404
from recipes.models import Recipe
from django.http import Http404


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipes/pages/home.html', context=context)


def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.filter(
        category__id=category_id, is_published=True).order_by('-id'))

    context = {
        'recipes': recipes,
        'title': f'{recipes[0].category.name} - Category',
    }
    return render(request, 'recipes/pages/category.html', context=context)


def recipe(request, id_recipe):
    recipe = get_object_or_404(Recipe.objects.filter(
        id=id_recipe, is_published=True))

    context = {
        'recipe': recipe,
        'is_detail_page': True,
        'title': recipe.title
    }
    return render(request, 'recipes/pages/recipe_view.html', context=context)


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    context = {
        'title': f'Search for "{search_term}"',
        'search_term': search_term,
    }

    return render(request, 'recipes/pages/search.html', context=context)


"""Esse é apenas um teste de commit utilizando o terminal ao invés do app"""
