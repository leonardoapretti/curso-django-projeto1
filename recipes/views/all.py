from django.shortcuts import render, get_list_or_404, get_object_or_404
from recipes.models import Recipe
from django.http import Http404
from django.db.models import Q
from utils.pagination import make_pagination
import os

PER_PAGE = os.environ.get('PER_PAGE', 6)


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

    recipes = Recipe.objects.filter(
        # a classe Q serve para implementar consultas complexas ao DB. Documentação: https://docs.djangoproject.com/en/5.0/topics/db/queries/
        # contains é Case Sensitive, icontains não é
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        ),
        is_published=True
    ).order_by('title')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    context = {
        'title': f'Search for "{search_term}"',
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
    }

    return render(request, 'recipes/pages/search.html', context=context)


"""Esse é apenas um teste de commit utilizando o terminal ao invés do app"""
