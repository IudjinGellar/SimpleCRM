from django.shortcuts import render, redirect
from ..models import Person
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from core.forms import PersonForm


class AddPersonView(LoginRequiredMixin, View):
    template = 'core/add_person.html'
    login_url = 'login'

    def get(self, request, id=0):
        '''get add_person page, if id=0 - blank,
         if id>0 - with current data about Person'''
        dictionary = {}
        if id == 0:
            dictionary['person_form'] = PersonForm()
            return render(request, self.template, dictionary)
        elif id > 0:
            person = Person.objects.get(id=id)
            dictionary['person_form'] = PersonForm(instance=person)
            return render(request, self.template, dictionary)

    def post(self, request, id=0):
        '''write new Person data:
                if id=0, add new Person with request data,
                    return redirect to the new person page;
                if id>0, redact current Person data,
                    return redirect to person page with message
                    about status of apply new data.'''
        if id == 0:
            person_form = PersonForm(request.POST)
            if person_form.is_valid():
                person = person_form.save()
            id = person.id
            out_message = 'Succesfully added'
            return redirect(to=f'/person/{id}?message={out_message}')
        elif id > 0:
            db_record = Person.objects.get(id=id)
            person_form = PersonForm(request.POST, instance=db_record)
            is_new_data = person_form.has_changed()
            message = None
            if person_form.is_valid():
                person_form.save()
                if is_new_data:
                    message = 'succesifully updated'
                else:
                    message = 'No new data'
            else:
                message = 'exception on save record'
            return redirect(to=f'/person/{id}?message={message}')
