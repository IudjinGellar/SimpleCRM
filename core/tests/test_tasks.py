from django.test import TestCase
from django.contrib.auth.models import User
from service.fill_DB import mim_do_persons, do_comments
from core.tasks import statistic, send_message


class Test_tasks(TestCase):

    @classmethod
    def setUpTestData(cls):
        for person in mim_do_persons(10, True):
            person.save()
        do_comments(50)
        test_user = User.objects.create_user(username='test', password='test')
        test_user.save()

    def login_test_user(self):
        self.client.login(username='test', password='test')

    def test_statistic(self):
        self.login_test_user()
        result = statistic()
        with open('service/objects_counter.txt', 'r') as file:
            data = file.read().split('\n')
            self.assertEquals(data[-2]+'\n', result)

    def test_sender(self):
        self.login_test_user()
        result = send_message('test_message')
        self.assertEquals(result, 'Message sending')
