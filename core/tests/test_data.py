from core.models import Person, Comment


def get_test_person():
    person = Person(name='Иван',
                    patronymic='Иванович',
                    surname='Иванов',
                    first_phone_number='79998887766',
                    second_phone_number='79991112233',
                    first_email='example@example.com',
                    second_email='email@email.com',
                    simple_comment='This is simple comment for test')
    return person


def get_test_comment():
    comment = Comment(made_for=Person.objects.all()[0],
                      comment='This is a test comment')
    return comment
