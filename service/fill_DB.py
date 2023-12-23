

def mim_do_persons(number=50, return_obj=False, no_save=False):
    from mimesis import Person as mim_Person
    from mimesis.locales import Locale
    from mimesis.enums import Gender
    from mimesis.builtins import RussiaSpecProvider
    from core.models import Person
    mim_person = mim_Person(Locale.RU)
    genders = [Gender.FEMALE, Gender.MALE]
    patronymics = RussiaSpecProvider()
    if return_obj:
        peoples = []
    for i in range(number):
        gender = genders[i % 2]
        new_person = Person(name=mim_person.name(gender=gender),
                            patronymic=patronymics.patronymic(gender=gender),
                            surname=mim_person.last_name(gender=gender),
                            first_phone_number=''.join(
                                [x for x in mim_person.phone_number()
                                 if x.isdigit()]),
                            second_phone_number=''.join(
                                [x for x in mim_person.phone_number()
                                 if x.isdigit()]),
                            first_email=mim_person.email(),
                            second_email=mim_person.email(),
                            simple_comment=f'This is simple comment {i}')
        if not no_save:
            new_person.save()
        if return_obj:
            peoples.append(new_person)
    if return_obj:
        return peoples


def do_comments(number=500):
    import random
    message = 'this is random comment and %s '
    from core.models import Comment, Person
    list_persons = Person.objects.all()
    from string import ascii_lowercase
    ascii_lowercase = ascii_lowercase + '          '
    for i in range(number):
        line = [random.choice(ascii_lowercase) for x in range(50)]
        comm = Comment(made_for=random.choice(list_persons),
                       comment=message % ''.join(line))
        comm.save()


def filler():
    mim_do_persons()
    do_comments()
