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

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            slug='one', title=title1, author_data={'username': 'one'}
        )

        recipe2 = self.make_recipe(
            slug='two', title=title2, author_data={'username': 'two'}
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        """IMPORTANTE - o atributo context da response é responsável por buscar os models criados pelo teste na base de dados provisória"""
        context1 = response1.context['recipes']
        context2 = response2.context['recipes']
        context_both = response_both.context['recipes']

        """A receita um deve estar no contexto 1"""
        self.assertIn(recipe1, context1)
        """A receita 2 não deve estar no contexto 1"""
        self.assertNotIn(recipe2, context1)

        """A receita dois deve estar no contexto 2"""
        self.assertIn(recipe2, context2)
        """A receita 1 não deve estar no contexto 2"""
        self.assertNotIn(recipe1, context2)

        self.assertIn(recipe1, context_both)
        self.assertIn(recipe2, context_both)

    def test_recipe_search_can_find_recipe_by_description(self):
        description1 = 'This is description one'
        description2 = 'This is description two'

        recipe1 = self.make_recipe(
            slug='d1', description=description1, author_data={'username': 'one'}, title='Recipe 1'
        )

        recipe2 = self.make_recipe(
            slug='d2', description=description2, author_data={'username': 'two'}, title='Recipe 2'
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={description1}')
        response2 = self.client.get(f'{search_url}?q={description2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])
