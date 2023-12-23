from django.test import TestCase
from django.contrib.auth.models import User


class TestLoginLogout(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='test', password='test')

    def login_test_user(self):
        self.client.login(username='test', password='test')

    def test_login_view_GET(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        self.login_test_user()
        response = self.client.get('/accounts/login/')
        self.assertNotEqual(response.status_code, 200)

    def test_login_view_POST(self):
        message = {}
        message['username'] = 'test'
        message['password'] = 'test'
        response = self.client.post('/accounts/login/', message)
        self.assertEqual(response.status_code, 302)
        # проверка доступа к main_page
        response = self.client.get('/core/')
        self.assertEqual(response.status_code, 200)

    def test_logout_view_GET(self):
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 302)
        self.login_test_user()
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 200)

    def test_logout_view_POST(self):
        message = {'logout': ''}
        self.login_test_user()
        self.client.post('/accounts/logout/', message)
        response = self.client.get('/core/')
        self.assertEqual(response.status_code, 302)
