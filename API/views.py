from django.http import HttpResponse, JsonResponse
# from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from core.models import Person, Comment, Functions
from API.serializers import PersonSerializer, AllPersonsSerializer, CommentSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.middleware import csrf


class APIAuth(APIView):
    def post(self, request):
        print('in post')
        message = Functions.get_message(request.POST)
        print(message)
        username = message['username']
        password = message['password']
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                token = csrf.get_token(request)
                response = JsonResponse({'csrfmiddlewaretoken': str(token)})
                response['status'] = 200
                return response
            else:
                return HttpResponse(status=404)
        else:
            return HttpResponse(status=400)


class APILogOut(APIView, LoginRequiredMixin):
    def post(self, request):
        logout(request)
        return HttpResponse(status=200)


class APIIsAuth(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return JsonResponse({'user': str(request.user),
                                'authenticated': 'True'})
        else:
            return JsonResponse({'user': 'None',
                                'authenticated': 'False'})


class APIAllPersonsView(APIView):
    def get(self, request):
        'предоставить все записи Person в виде id и ФИО'
        persons = Person.objects.all()
        serializer = AllPersonsSerializer(persons, many=True)
        return JsonResponse(serializer.data, safe=False)


class APIPersonView(APIView):
    def get_person(self, id):
        try:
            person = Person.objects.get(id=id)
            return person
        except Person.DoesNotExist:
            return None

    def get(self, request, id):
        'предоставить конкретную запись Person по id'
        person = self.get_person(id)
        if person:
            serializer = PersonSerializer(person)
            return JsonResponse(serializer.data)
        else:
            return HttpResponse(status=404)


class APICommentsView(APIView):
    def get_comments(self, person_id):
        comments = Comment.objects.filter(made_for=person_id)
        print(comments)
        return comments

    def get(self, request, person_id):
        'получить все комментарии для выбранного Person по id'
        comments = self.get_comments(person_id)
        if comments:
            serializer = CommentSerializer(comments, many=True)
            print(serializer.data)
            return JsonResponse(serializer.data, safe=False)