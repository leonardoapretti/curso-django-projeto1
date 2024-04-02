from django.views import View
from recipes.models import Recipe
from authors.forms import AuthorRecipeForm
from django.http.response import Http404
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    # esse método está na classe View. Por padrão o django inicializa as variáveis da view e, em seguida, tenta descobrir qual o método correto da view (GET OU POST) através do método dispatch da classe View.
    # Aqui, nós estamos decorando este método com lofin_required para que, caso não esteja logado, ele nem busque o método correto e apenas redirecione para a página de login
    name='dispatch'
)
class DashboardRecipe(View):
    def get_recipe(self, id):
        recipe = None
        if id:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id,
            ).first()
            if not recipe:
                raise Http404()
        return recipe

    def render_recipe(self, context):
        return render(self.request, 'authors/pages/dashboard_recipe.html', context)

    def get(self, request, id=None):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(
            instance=recipe,
        )
        context = {
            'form': form,
        }
        return self.render_recipe(context)

    def post(self, request, id=None):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(
            request.POST or None,
            files=request.FILES or None,
            instance=recipe,
        )
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False
            recipe.save()
            if id is None:
                messages.success(
                    request, 'Your recipe has been created! Update it if you need.')
            else:
                messages.success(request, 'Your recipe has been updated!')
            return redirect(reverse('authors:dashboard_recipe_edit', args=(recipe.id,)))
        context = {
            'recipe': recipe,
            'form': form,
        }
        return self.render_recipe(context)
