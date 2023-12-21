from django.test import TestCase
import requests

print('Required local server')
USERNAME = ''
PASSWORD = ''
HOST = 'http://127.0.0.1:8000/api/'
if not USERNAME:
    USERNAME = input('Input username: ')
if not PASSWORD:
    PASSWORD = input('Input password: ')


class test_API(TestCase):
    def test_run(self):
        token = self.auth()
        self.logout(token)
        self.isauth(False)

    def auth(self):
        adress = HOST + 'auth'
        data = {'username': USERNAME,
                'password': PASSWORD}
        response = requests.post(adress, data)
        r_data = response.json()
        self.assertIs('csrfmiddlewaretoken' in r_data.keys(), True)
        return r_data

    def logout(self, token):
        adress = HOST + 'logout'
        response = requests.post(adress, token)
        self.assertIs(response.status_code, 200)

    def isauth(self, isauthvalue):
        adress = HOST + 'isauth'
        response = requests.get(adress)
        data = response.json()
        self.assertIs(eval(data['authenticated']), isauthvalue)
