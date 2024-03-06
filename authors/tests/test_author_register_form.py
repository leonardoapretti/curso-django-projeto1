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
        ('username', 'Your username'),
        ('first_name', 'Ex: John'),
        ('last_name', 'Ex: Smith'),
        ('email', 'Your e-mail'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        current_placeholder = self.form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('username', 'Username must have letters, numbers or one of those @ . + - _'
         'The length should be between 4 and 150 characters.'),
        ('email', 'Enter a valid email'),
        ('password', 'Password must have at least one upper case letter, '
         'one lowercase letter and one number.'),
    ])
    def test_fields_help_text(self, field, help_text):
        current = self.form[field].field.help_text
        self.assertEqual(help_text, current)

    @parameterized.expand([
        ('password', 'required', 'Password must not be empty'),
        ('username', 'required', 'This field must not be empty'),

    ])
    def test_fields_error_messages(self, field, error_message, needed):
        current = self.form[field].field.error_messages[error_message]
        self.assertEqual(
            needed, current)

    @parameterized.expand([
        ('username', 'Type your username'),
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('email', 'Type your email here'),
        ('password', 'Password'),
        ('password2', 'Confirm your password'),
    ])
    def test_fields_labels(self, field, needed):
        current = self.form[field].field.label
        self.assertEqual(needed, current)

    def test_email_field_is_email_field(self):
        current = self.form['email'].widget_type
        self.assertEqual('email', current)

    def test_email_field_input_is_email_input(self):
        current = self.form['email'].field.widget.input_type
        self.assertEqual('email', current)

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
            'password2': 'Str0ngP@ssword1',
        }
        self.url = reverse('authors:create')

        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('email', 'E-mail must not be empty'),
        ('password', 'Password must not be empty'),
        ('password2', 'Confirm your password must not be empty'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        # follow=True serve para o teste continuar o fluxo com o redirect
        response = self.client.post(self.url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_min_length_should_be_4(self):
        self.form_data['username'] = 'abc'
        response = self.client.post(self.url, data=self.form_data, follow=True)
        expected_error_message = 'Username must have at least 4 characters.'
        self.assertIn(expected_error_message, response.content.decode('utf-8'))
        self.assertIn(expected_error_message,
                      response.context['form'].errors.get('username'))

    def test_username_max_length_should_be_150(self):
        self.form_data['username'] = 'a' * 151
        response = self.client.post(self.url, data=self.form_data, follow=True)
        expected_error_message = 'Username must not be more than 150 characters.'
        self.assertIn(expected_error_message, response.content.decode('utf-8'))
        self.assertIn(expected_error_message,
                      response.context['form'].errors.get('username'))

    def test_password_field_has_upper_lower_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        response = self.client.post(self.url, data=self.form_data, follow=True)
        expected_error_message = (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )
        self.assertIn(expected_error_message, response.content.decode('utf-8'))
        self.assertIn(expected_error_message,
                      response.context['form'].errors.get('password'))

        self.form_data['password'] = '@Abc1234'
        response = self.client.post(self.url, data=self.form_data, follow=True)
        self.assertNotIn(expected_error_message,
                         response.context['form'].errors.get('password'))

    def test_valid_password_fields_are_equal(self):
        self.form_data['password'] = '@Bcd1234'
        self.form_data['password2'] = '@Bcd12345'
        response = self.client.post(self.url, data=self.form_data, follow=True)

        expected_error_message = 'Passwords must be equal'
        self.assertIn(expected_error_message,
                      response.context['form'].errors.get('password'))
        self.assertIn(expected_error_message,
                      response.context['form'].errors.get('password2'))
        self.assertIn(expected_error_message, response.content.decode('utf-8'))

        self.form_data['password'] = '@Bcd1234'
        self.form_data['password2'] = '@Bcd1234'
        response = self.client.post(self.url, data=self.form_data, follow=True)

        self.assertNotIn(expected_error_message,
                         response.content.decode('utf-8'))
        self.assertIsNone(response.context['form'].errors.get('password'))
        self.assertIsNone(response.context['form'].errors.get('password2'))

    def test_email_field_must_be_unique(self):
        self.form_data['email'] = 'email@email.com'
        self.client.post(self.url, data=self.form_data, follow=True)
        response = self.client.post(
            self.url, data=self.form_data, follow=True)

        msg = 'User e-mail is already in use'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg,
                      response.context['form'].errors.get('email'))

        ...
