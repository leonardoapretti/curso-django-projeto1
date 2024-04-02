from django.views.generic import ListView
from utils.pagination import make_pagination
from recipes.models import Recipe
import os

PER_PAGE = os.environ.get('PER_PAGE', 6)

# CRIA A CLASSE BASE DE RECIPES


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['id']
    template_name = 'recipes/pages/home.html'

    # MANIPULA A QUERY_SET (POR PADRÃO O DJANDO RECUPERA TODOS OS OBJETOS DO MODEL)
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        filtered_qs = qs.filter(
            is_published=True,
        )
        return filtered_qs

    # MANIPULA O CONTEXTO (SERVE PARA ATUALIZAR O CONTEXTO DA APLICAÇÃO)
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE,
        )
        ctx.update(
            {'recipes': page_obj, 'pagination_range': pagination_range}
        )
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        filtered_qs = qs.filter(
            category__id=self.kwargs.get('category_id')
        )
        return filtered_qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        title = ctx.get('object_list')[0].category.name
        ctx.update({
            'title': title,
        })
        return ctx
