
# from django.test import LiveServerTestCase # essa classe sobe o servidor mas não carrega os arquivos estáticos (css, js e outros). Mais rápida
# Sobe o servidor com arquivos estáticos
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
import time


class RecipeBaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = make_chrome_browser()
        self.browser.get(self.live_server_url)
        return super().setUp()

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=1):
        time.sleep(seconds)
