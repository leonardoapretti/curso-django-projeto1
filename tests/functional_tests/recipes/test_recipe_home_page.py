
from selenium.webdriver.common.by import By
from .base import RecipeBaseFunctionalTest
import pytest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_messages(self):
        self.browser.get(self.live_server_url)
        self.make_recipe()
        body = self.browser.find_element(By.TAG_NAME, 'body')
        # self.sleep()
        self.assertIn('Nenhuma receita para mostrar', body.text)
