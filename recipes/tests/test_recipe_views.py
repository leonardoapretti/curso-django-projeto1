from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase
# pip install pytest-watch + comando ptw = serve para rodar os testes em loop. Sempre que salvar o arquivo ele atualiza o teste


class RecipeViewsTest(RecipeTestBase):

    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertTrue(view.func is views.home)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('Nenhuma receita para mostrar',
                      response.content.decode('utf-8'))

    def test_recipe_home_template_loads_recipes(self):
        # need a recipe for this test
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        # check if one recipe exists
        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 4}))
        self.assertTrue(view.func is views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 4})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id_recipe': 4}))
        self.assertTrue(view.func is views.recipe)

    def test_recipe_detail_view_returns_404_if_not_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id_recipe': 2}))
        self.assertEqual(response.status_code, 404)
