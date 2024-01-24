from django.forms import ModelForm
from core.models import Person


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = [field for field in Person.get_fields() if field != 'id']
