from django.test import TestCase as DjangoTestCase
from django.urls import reverse


class AuthorLoginCreateViewIntegrationTest(DjangoTestCase):
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
            'username': 'user',
            'password': 'Str0ngP@ssword1',
        }
        self.login_url = reverse('authors:login_create')
        return super().setUp()

    def test_user_test_is_correctly_created(self):
        self.assertEqual(
            self.create_user_response.request['PATH_INFO'], '/authors/login/')

    def test_login_create_view_raises_http_404_if_method_not_post(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 404)

    def test_login_create_view_form_is_not_valid(self):
        self.login_form_data['username'] = ''
        response = self.client.post(
            self.login_url, data=self.login_form_data, follow=True)
        self.assertIn('Invalid username or password',
                      response.content.decode('utf-8'))

    def test_login_create_view_user_is_authenticated(self):
        response = self.client.post(
            self.login_url, data=self.login_form_data, follow=True)
        self.assertIn('You are logged in', response.content.decode('utf-8'))

    def test_login_create_view_user_is_not_authenticated(self):
        self.login_form_data['username'] = 'abcde'
        response = self.client.post(
            self.login_url, data=self.login_form_data, follow=True)
        self.assertIn('Invalid credentials.', response.content.decode('utf-8'))
        ...
