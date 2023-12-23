from django.test import TestCase
from core.models import Person, Comment
from core.tests.test_data import get_test_person, get_test_comment


class PersonModelTest(TestCase):

    def get_person_db(self):
        person_db = Person.objects.get(id=1)
        return person_db

    def setUp(self):
        person_db = get_test_person()
        person_db.save()

    def test_all_fields(self):
        person_db = self.get_person_db()
        person_db_fields = person_db.get_fields()
        person_obj = get_test_person()
        for field in person_db_fields:
            if field == 'id':
                continue
            else:
                self.assertEqual(eval('person_db.'+field),
                                 eval('person_obj.'+field))


class CommentModelTest(TestCase):

    def setUp(self):
        person = get_test_person()
        person.save()
        comment = get_test_comment()
        comment.save()

    def test_all_fields(self):
        comment = get_test_comment()
        comment_db = Comment.objects.get(id=1)
        for field in Comment.get_fields():
            if field in ('id', 'comm_date'):
                self.assertTrue(eval('comment_db.'+field))
            else:
                self.assertEqual(eval('comment.'+field),
                                 eval('comment_db.'+field))
