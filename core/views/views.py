from django.shortcuts import render
from django.http import HttpResponse
from ..models import Person, Comment
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def main_page(request):
	'return simple page if user do not use required page name'
	return render(request, 'core/main_page.html')

