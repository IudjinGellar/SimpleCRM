from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('', include('core.urls')),
    path('core/', include('core.urls')),
    path('api/', include('API.urls')),
]
