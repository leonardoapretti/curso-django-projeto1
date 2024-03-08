# from django.test import LiveServerTestCase # essa classe sobe o servidor mas não carrega os arquivos estáticos (css, js e outros). Mais rápida
# Sobe o servidor com arquivos estáticos
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser

from selenium.webdriver.common.by import By

import time


class RecipeHomePageFunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = make_chrome_browser()
        self.browser.get(self.live_server_url)
        return super().setUp()

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)

    def test_de_test(self):
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Nenhuma receita para mostrar', body.text)
        self.sleep()
