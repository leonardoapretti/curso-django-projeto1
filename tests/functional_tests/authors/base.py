from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from time import sleep
from utils.browser import make_chrome_browser


class AuthorsBaseFunctionalTest(StaticLiveServerTestCase):
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
