from django.views import View
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin


class Logout(LoginRequiredMixin, View):
	template = 'accounts/logout.html'
	login_url = 'login'
	def get(self, request):
		dictionary = {}
		dictionary['message'] = f'Press logout button to logout from account {request.user.username}'
		return render (request, self.template, dictionary)
	def post(self, request):
		if 'logout' in request.POST.keys() :
			logout(request)
			return redirect('/accounts/login?message=Successfully logout')
