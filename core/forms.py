from django.forms import ModelForm
from core.models import Person, PersonFile


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = [field for field in Person.get_fields() if field != 'id']


class PersonFileForm(ModelForm):
    class Meta:
        model = PersonFile
        fields = ('name', 'file')
