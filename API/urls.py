from django.urls import path, re_path
from .views import APIAllPersonsView, \
    APIPersonView, APICommentsView, APIAuth, \
    APILogOut, APIIsAuth
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title='SimpleCRM API',
        description='API for project SimpleCRM',
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    path('auth/', APIAuth.as_view()),
    path('logout/', APILogOut.as_view()),
    path('isauth/', APIIsAuth.as_view(), name='isauth'),
    path('all/', APIAllPersonsView.as_view()),
    path('person/<int:id>/', APIPersonView.as_view()),
    path('comments/<int:person_id>/', APICommentsView.as_view()),
    ]
