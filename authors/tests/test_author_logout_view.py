from django.test import TestCase as DjangoTestCase
from django.urls import reverse


class AuthorsLogoutViewIntegrationTest(DjangoTestCase):
    def setUp(self) -> None:
        self.create_user_form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@email.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1',
        }
        self.register_url = reverse('authors:register_create')
        self.create_user_response = self.client.post(
            self.register_url, data=self.create_user_form_data, follow=True)

        self.login_form_data = {
            'username': self.create_user_form_data['username'],
            'password': self.create_user_form_data['password'],
        }
        self.login_url = reverse('authors:login_create')
        self.user_login_response = self.client.post(
            self.login_url, data=self.login_form_data, follow=True)
        self.logout_url = reverse('authors:logout')
        self.logout_form_data = {
            'username': self.create_user_form_data['username']
        }
        return super().setUp()

    def test_logout_view_redirects_to_login_view_if_method_is_not_post(self):
        response = self.client.get(self.logout_url, follow=True)
        self.assertIn('Invalid logout request.',
                      response.content.decode('utf-8'))

    def test_logout_view_redirects_to_login_view_if_not_logged_user_tries_logout(self):
        self.logout_form_data['username'] = 'teste'
        response = self.client.post(
            self.logout_url, data=self.logout_form_data, follow=True)
        self.assertIn('Invalid logout user.', response.content.decode('utf-8'))

    def test_logout_view_logout_logged_in_user(self):
        response = self.client.post(
            self.logout_url, data=self.logout_form_data, follow=True)
        self.assertIn('Logged out successfully.',
                      response.content.decode('utf-8'))
