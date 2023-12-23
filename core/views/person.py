from django.shortcuts import render, redirect
from ..models import Person, Comment, Functions
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class PersonView(LoginRequiredMixin, View):
    template = 'core/person.html'
    login_url = 'login'

    def get(self, request, id):
        'display Person data and his Comments, message if have it'
        dictionary = {}
        person = Person.objects.get(id=id)
        dictionary['comments'] = (Comment.objects.filter(made_for_id=id) or [])
        dictionary['person'] = person.get_attrs_values()
        if 'message' in request.GET.keys():
            dictionary['message'] = \
                Functions.get_message(request.GET)['message']
        return render(request, self.template, dictionary)

    def post(self, request, id):
        'add new Comment or File to Person'
        def new_comment(comment, person):
            new_comment = Comment(made_for=person, comment=comment)
            new_comment.save()

        message = Functions.get_message(request.POST)
        person = Person.objects.get(id=id)
        if 'comment' in message:
            new_comment(message['comment'], person)
        return redirect(f'/person/{id}')
