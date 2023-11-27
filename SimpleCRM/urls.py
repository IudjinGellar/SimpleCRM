
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('', include('core.urls')),
    path('core/', include('core.urls')) ,
]
