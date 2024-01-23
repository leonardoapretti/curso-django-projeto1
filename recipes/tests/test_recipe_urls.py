from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    # Ser super descritivo no nome dos testes
    def test_recipe_home_url_is_correct(self):
        home_url = reverse('recipes:home')
        self.assertEqual(home_url, '/')

    def test_recipe_category_url_is_correct(self):
        url = reverse('recipes:category', kwargs={'category_id': 4})
        self.assertEqual(url, '/recipes/category/4/')

    def test_recipe_detail_url_is_correct(self):
        url = reverse('recipes:recipe', kwargs={'id_recipe': 4})
        self.assertEqual(url, '/recipes/4/')

    def test_recipe_search_url_is_correct(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')
