# essa classe sobe o servidor mas não carrega os arquivos estáticos (css, js e outros). Mais rápida
# from django.test import LiveServerTestCase
from time import sleep

# Sobe o servidor com arquivos estáticos
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser

from recipes.tests.test_recipe_base import RecipeMixin


class RecipeBaseFunctionalTest(StaticLiveServerTestCase, RecipeMixin):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        # self.browser.get(self.live_server_url + 'authors/register/')
        # self.browser.get('http://127.0.0.1:8000/')
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=3):
        sleep(seconds)
