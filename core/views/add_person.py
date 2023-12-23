from django.shortcuts import render, redirect
from ..models import Person, Functions
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class AddPersonView(LoginRequiredMixin, View):
    template = 'core/add_person.html'
    login_url = 'login'

    def get(self, request, id=0):
        '''get add_person page, if id=0 - blank,
         if id>0 - with current data about Person'''
        dictionary = {}
        if id == 0:
            return render(request, self.template, dictionary)
        elif id > 0:
            person = Person.objects.get(id=id)
            dictionary['person'] = person.get_attrs_values()
            return render(request, self.template, dictionary)

    def post(self, request, id=0):
        '''write new Person data:
                if id=0, add new Person with request data,
                    return redirect to the new person page;
                if id>0, redact current Person data,
                    return redirect to person page with message
                    about status of apply new data.'''
        message = Functions.get_message(request.POST)
        if id == 0:
            person = Person()
            person.set_attrs(message)
            person.save()
            id = person.id
            out_message = 'Succesfully added'
            return redirect(to=f'/person/{id}?message={out_message}')
        elif id > 0:
            db_record = Person.objects.get(id=id)
            person = Person()
            person.set_attrs(message)
            is_new_data = False
            message = None
            for attr in db_record.get_fields():
                try:
                    if attr == 'id':
                        continue
                    elif eval('db_record.'+attr) == eval('person.'+attr):
                        continue
                    else:
                        is_new_data = True
                        exec('db_record.'+attr+'=person.'+attr)
                except AttributeError:
                    continue
            if is_new_data:
                try:
                    db_record.save()
                    message = 'succesifully updated'
                except Exception:
                    message = 'exception on save record'
            else:
                message = 'no new data'
            return redirect(to=f'/person/{id}?message={message}')
