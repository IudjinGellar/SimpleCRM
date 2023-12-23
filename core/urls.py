from django.urls import path
from .views import views, PersonView, SearchView, AddPersonView

urlpatterns = [
    path('person/<int:id>', PersonView.as_view(), name='person'),
    path('search/<int:list_number>', SearchView.as_view(), name='search'),
    path('add_person/<int:id>', AddPersonView.as_view(), name='add_person'),
    path('', views.main_page, name='main'),
    ]
