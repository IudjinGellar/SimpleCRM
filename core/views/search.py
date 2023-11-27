from django.shortcuts import render
from django.http import HttpResponse
from ..models import Person, Comment, Functions
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

class SearchView(LoginRequiredMixin, View):
	template = 'core/search.html'
	login_url = 'login'
	def get(self, request, list_number=0):
		''' return page with list peoples:
				if not search_data: return Peoples where id from 0 to 10;
				if search_list>0: return Peoples corresponding numbers;
				if have search_data:
					try to find Person by name or phone number
					return list Peoples
		'''
		dictionary = {}
		message = Functions.get_message(request.GET)
		if not message:
			dictionary['peoples'] = Person.objects.all()[list_number*10:list_number*10+10]
			dictionary['current_list'] = list_number
		else:
			search_name = message['search_value']
			print(search_name)
			search_name = search_name.replace('+','').replace('-','').replace(' ','')
			if search_name.isdigit():
				result = \
				Person.objects.filter(first_phone_number__contains=search_name).order_by('surname')|\
				Person.objects.filter(second_phone_number__contains=search_name).order_by('surname')
			else:
				result = \
				Person.objects.filter(surname__icontains=search_name).order_by('surname')|\
				Person.objects.filter(first_name__icontains=search_name).order_by('surname')
			dictionary['peoples'] = result
			dictionary['search_value'] = message['search_value']
		return render(request, self.template, dictionary)
