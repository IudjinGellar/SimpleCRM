from django.urls import path
from .views import APIAllPersonsView, \
    APIPersonView, APICommentsView, APIAuth, \
    APILogOut, APIIsAuth


urlpatterns = [
    path('auth', APIAuth.as_view()),
    path('logout', APILogOut.as_view()),
    path('isauth', APIIsAuth.as_view(), name='isauth'),
    path('all', APIAllPersonsView.as_view()),
    path('person/<int:id>', APIPersonView.as_view()),
    path('comments/<int:person_id>', APICommentsView.as_view()),
    ]
