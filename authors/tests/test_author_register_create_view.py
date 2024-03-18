from django.test import TestCase as DjangoTestCase
from django.urls import reverse


class AuthorsViewsIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.url = reverse('authors:register_create')
        return super().setUp(*args, **kwargs)

    def test_register_create_view_raises_http_404_if_response_method_is_not_post(self):
        response = self.client.get(self.url)
        self.assertEqual(404, response.status_code)
