from django.shortcuts import render, redirect
from ..models import Person, Comment, Functions, PersonFile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from core.forms import PersonForm, PersonFileForm


class PersonView(LoginRequiredMixin, View):
    template = 'core/person.html'
    login_url = 'login'

    def get(self, request, id):
        'display Person data and his Comments, message if have it'
        dictionary = {}
        person = Person.objects.get(id=id)
        person_form = PersonForm(instance=person)
        dictionary['comments'] = (Comment.objects.filter(made_for_id=id) or [])
        dictionary['person_form'] = person_form
        dictionary['id'] = id
        files = PersonFile.objects.filter(owner_id=person) or None
        if files:
            dictionary['files'] = files
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
            message = 'Add new comment'
        elif 'filename' in message:
            try:
                file = request.FILES['file']
                if file:
                    new_file = PersonFile(name=message['filename'],
                                          file=file,
                                          owner=person)
                    new_file.save()
                    message = 'Add file'
                else:
                    message = 'No data!'
            except Exception:
                message = 'Exception on save'
        return redirect(f'/person/{id}/?message={message}')
