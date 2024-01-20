from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth.models import User
from core.models import Person, Comment
from core.tests.test_data import get_test_person
from service.fill_DB import mim_do_persons


class TestCoreViews(TestCase):
    number_of_persons = None
    std_person_id = None
    last_id = None

    @classmethod
    def setUpTestData(cls):
        # создает первого шаблонного Person
        # остальные со случайными данными
        person = get_test_person()
        person.save()
        cls.std_person_id = person.id
        number_of_persons = 1
        for person in mim_do_persons(10, True):
            person.save()
            number_of_persons += 1
        cls.last_id = person.id
        cls.number_of_persons = number_of_persons
        test_user = User.objects.create_user(username='test', password='test')
        test_user.save()
        # print(Person.objects.all())

    def login_test_user(self):
        self.client.login(username='test', password='test')

    def test_url_exist(self):
        self.login_test_user()
        for number in range(self.std_person_id, self.last_id):
            response = self.client.get(f'/core/person/{number}/')
            self.assertEqual(response.status_code, 200)
        for number in range((self.number_of_persons//10)):
            response = self.client.get(f'/core/search/{number}/')
            self.assertEqual(response.status_code, 200)
        for number in range(self.std_person_id, self.last_id):
            response = self.client.get(f'/core/add_person/{number}/')
            self.assertEqual(response.status_code, 200)
        response = self.client.get('/core/add_person/0/')
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_required_login_GET(self):
        # without login
        id = self.std_person_id
        paths = [f'/person/{id}/', f'/search/{id}/', '/add_person/0/', '/']
        for _path in paths:
            _path = '/core' + _path
            response = self.client.get(_path)
            self.assertNotEqual(response.status_code, 200)
        # with login
        self.login_test_user()
        for _path in paths:
            _path = '/core' + _path
            response = self.client.get(_path)
            self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_person_POST(self):
        self.login_test_user()
        # person view, add comment
        request_comment = {'comment': 'test comment'}
        self.client.post(f'/core/person/{self.std_person_id}/',
                         request_comment)
        comment = Comment.objects.get(
            made_for=Person.objects.get(id=self.std_person_id))
        self.assertEqual(comment.comment, request_comment['comment'])
        self.client.logout()

    def test_add_person_POST(self):
        self.login_test_user()
        # test add new (id==0)
        person_to_add = mim_do_persons(1, return_obj=True, no_save=True)[0]
        attrs = person_to_add.get_attrs_values()
        attrs['id'] = 0
        self.client.post('/core/add_person/0/', attrs, id=0)
        person = Person.objects.get(surname=person_to_add.surname)
        self.assertTrue(person.id)
        # test existing person (id>0)
        person = Person.objects.get(surname=attrs['surname'])
        attrs = person.get_attrs_values()
        id = person.id
        new_surname = 'Петров'
        attrs['surname'] = new_surname
        self.client.post(f'/core/add_person/{id}/', attrs)
        new_data_person = Person.objects.get(id=id)
        self.assertEqual(
            new_data_person.surname, new_surname)
        self.client.logout()

    def test_search_with_data_GET(self):
        self.login_test_user()
        # search by name, surname, phone_numbers
        person = Person.objects.get(id=self.std_person_id)
        name = person.name
        patronymic = person.patronymic
        surname = person.surname
        search_value = f'{surname} {name} {patronymic}'
        first_phone_number = person.first_phone_number
        second_phone_number = person.second_phone_number
        for any in name, surname, first_phone_number, second_phone_number:
            message = {}
            message['search_value'] = any
            response = self.client.get('/core/search/0/', message)
            self.assertTrue(search_value in response.content.decode())
        self.client.logout()

    @patch('core.tasks.statistic.apply_async')
    def test_statistic_view(self, statistic):
        self.login_test_user()
        response = self.client.get('/core/worker/')
        self.assertEquals(response.status_code, 200)

    @patch('core.tasks.send_message.apply_async')
    def test_sender_view(self, send_message):
        self.login_test_user()
        response = self.client.get('/core/sender/')
        self.assertEquals(response.status_code, 200)
