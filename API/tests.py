from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Person, Comment
from core.tests.test_data import get_test_person, get_test_comment
from service.fill_DB import mim_do_persons, do_comments


class test_API(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test', password='test')
        get_test_person().save()
        get_test_comment().save()
        mim_do_persons(10)
        do_comments(50)

    def auth(self):
        message = {
            'username': 'test',
            'password': 'test'}
        response = self.client.post('/api/auth', message)
        token = response.json()
        return token

    def isauth(self):
        response = self.client.get('/api/isauth')
        return eval(response.json()['authenticated'])

    def test_auth_logout(self):
        token = self.auth()
        self.assertTrue('csrfmiddlewaretoken' in token.keys())
        self.assertTrue(self.isauth())
        self.client.post('/api/logout', token)
        self.assertFalse(self.isauth())

    def test_you_shall_not_pass(self):
        GET = self.client.get
        POST = self.client.post
        self.assertFalse(self.isauth())
        self.assertEqual(POST('/api/logout').status_code, 302)
        self.assertEqual(GET('/api/all').status_code, 302)
        self.assertEqual(GET('/api/person/1').status_code, 302)
        self.assertEqual(GET('/api/comments/1').status_code, 302)

    def test_all_view(self):
        token = self.auth()
        response = self.client.get('/api/all', token)
        response_data = response.json()
        persons_db = Person.objects.all().only('surname')
        surnames_db = [person.surname for person in persons_db]
        for person in response_data:
            self.assertTrue(person['surname'] in surnames_db)

    def test_api_person_view(self):
        token = self.auth()
        response = self.client.get('/api/person/1', token)
        response_data = response.json()
        person = Person.objects.get(id=1)
        person_data = person.get_attrs_values()
        for key, value in response_data.items():
            self.assertEqual(person_data[key], value)

    def test_comments_view(self):
        token = self.auth()
        response = self.client.get('/api/comments/1', token)
        response_data = response.json()
        person = Person.objects.get(id=1)
        for comment in response_data:
            self.assertEqual(comment['made_for'], person.id)
            self.assertTrue(comment['comm_date'])
        response_comments = [x['comment'] for x in response_data]
        comments = Comment.objects.filter(made_for=person)
        comments_data = [comment.comment for comment in comments]
        for sentence in response_comments:
            self.assertTrue(sentence in comments_data)
