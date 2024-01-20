from celery import shared_task
from core.models import Person, Comment
import datetime


@shared_task
def statistic():
    num_persons = Person.objects.all().count()
    num_comments = Comment.objects.all().count()
    dt = datetime.datetime.now()
    str_dt = dt.strftime('%Y-%m-%d')
    with open('service/objects_counter.txt', 'a') as file:
        line = f'{str_dt}| Persons: {num_persons}, Comments: {num_comments}\n'
        file.write(line)
    return line

@shared_task
def send_message(message):
    return 'Message sending'
