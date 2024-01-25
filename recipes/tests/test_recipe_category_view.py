from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase
from unittest import skip
# pip install pytest-watch + comando ptw = serve para rodar os testes em loop. Sempre que salvar o arquivo ele atualiza o teste


class RecipeCategoryViewTest(RecipeTestBase):

    """CATEGORY TESTS"""

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

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'

        # need a recipe for this test
        self.make_recipe(title=needed_title)
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        content = response.content.decode('utf-8')

        # check if one recipe exists
        self.assertIn(needed_title, content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False dont show"""
        # need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': recipe.category_id}))
        self.assertEqual(response.status_code, 404)
