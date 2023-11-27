from django.views import View
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from core.models import Functions

class Login(View):
	template = 'accounts/login.html'
	def get(self, request):
		'return login page'
		dictionary = {}
		message = Functions.get_message(request.GET)
		try : dictionary['message'] = message['message']
		except KeyError: pass
		if request.user.is_authenticated:
			dictionary['message'] = 'You logined now! Logout to change user!'
			return redirect ('accounts/logout/', dictionary)
		else:
			return render(request, self.template, dictionary)
	def post(self, request):
		dictionary = {}
		message = Functions.get_message(request.POST)
		username = message['username']
		password = message['password']
		if username and password:
			user = authenticate(username=username, password=password)
			if user:
				login(request, user)
				return redirect (to='main')
			elif user==None:
				dictionary['message'] = f'Wrong input'
				return render (request, self.template, dictionary) 
		else:
			dictionary['message'] = 'No input data!'
			return render (request, self.template, dictionary)