from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views

# pip install pytest-watch + comando ptw = serve para rodar os testes em loop. Sempre que salvar o arquivo ele atualiza o teste


class RecipeViewsTest(TestCase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertTrue(view.func is views.home)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 4}))
        self.assertTrue(view.func is views.category)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id_recipe': 4}))
        self.assertTrue(view.func is views.recipe)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')
