from django.test import TestCase
from django.urls import reverse

# pip install pytest-watch + comando ptw = serve para rodar os testes em loop. Sempre que salvar o arquivo ele atualiza o teste


class RecipeURLsTest(TestCase):
    # Ser super descritivo no nome dos testes
    def test_recipe_home_url_is_correct(self):
        home_url = reverse('recipes:home')
        self.assertEqual(home_url, '/')
