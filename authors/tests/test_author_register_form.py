from authors.forms import RegisterForm
from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from parameterized import parameterized
from django.urls import reverse


class AuthorRegisterFormUnitTest(TestCase):
    def setUp(self):
        self.form = RegisterForm()
        return super().setUp()

    @parameterized.expand([
        ('first_name', 'Ex: John'),
        ('last_name', 'Ex: Smith'),
        ('email', 'Your e-mail'),
        ('username', 'Your username'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        current_placeholder = self.form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('email', 'Enter a valid email'),
        ('password', 'Password must have at least one upper case letter, '
         'one lowercase letter and one number.'),
    ])
    def test_fields_help_text(self, field, help_text):
        current = self.form[field].field.help_text
        self.assertEqual(help_text, current)

    @parameterized.expand([
        ('password', 'required', 'Password must not be empty'),
        ('username', 'required', 'Esse campo é obrigatório, preencha novamente.'),
        ('username', 'max_length', 'Este campo deve ter menos de x caracteres.'),

    ])
    def test_fields_error_messages(self, field, error_message, needed):
        current = self.form[field].field.error_messages[error_message]
        self.assertEqual(
            needed, current)

    @parameterized.expand([
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('email', 'Type your email here'),
        ('username', 'Type your username'),
        ('password', 'Password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_labels(self, field, needed):
        current = self.form[field].field.label
        self.assertEqual(needed, current)

    @parameterized.expand([
        'password',
        'password2',
    ])
    def test_password_fields_are_password_inputs(self, field):
        password_widget_type = self.form[field].field.widget.input_type
        self.assertEqual('password', password_widget_type)

    @parameterized.expand([
        'password',
        'password2',
    ])
    def test_password_fields_are_required(self, field):
        password_is_required = self.form[field].field.required
        self.assertEqual(password_is_required, True)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@email.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword2',
        }

        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty'),
    ])
    def test_fields_cannot_be_empty(self, field):
        self.form_data[field] = ''
        msg = 'This field must not be empty'
        url = reverse('authors:create')
        # follow=True serve para o teste continuar o fluxo com o redirect
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        ...
