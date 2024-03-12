from .base import AuthorsBaseFunctionalTest
import pytest


@pytest.mark.functional_test
class AuthorsRegisterPageFunctionalTest(AuthorsBaseFunctionalTest):
    def test_the_test(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        self.sleep()
