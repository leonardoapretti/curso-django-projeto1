from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase

# pip install pytest-watch + comando ptw = serve para rodar os testes em loop. Sempre que salvar o arquivo ele atualiza o teste


class RecipeSearchViewTest(RecipeTestBase):
    """SEARCH TESTS"""

    def test_recipe_search_view_is_correct(self):
        url = reverse('recipes:search')
        view = resolve(url)
        self.assertIs(view.func, views.search)

    def test_recipe_search_view_returns_status_code_200(self):
        response = self.client.get(reverse('recipes:search') + '?q=Teste')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_recipe_search_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=Teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        response = self.client.get(reverse('recipes:search') + '?q=Teste')
        self.assertIn('Search for &quot;Teste&quot;',
                      response.content.decode('utf-8'))
