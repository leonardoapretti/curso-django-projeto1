
from selenium.webdriver.common.by import By
from .base import RecipeBaseFunctionalTest
import pytest
from django.urls import reverse


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_messages(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Nenhuma receita para mostrar', body.text)

    # esse teste não ta correto pois ele não encontra a receita criada

    # def test_recipe_home_page_with_recipes(self):
    #     self.browser.get(self.live_server_url)
    #     recipe = self.make_recipe()
    #     body = self.browser.find_element(By.TAG_NAME, 'body')

    #     self.assertNotIn('Nenhuma receita para mostrar', body.text)
