from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('', include('core.urls')),
    path('core/', include('core.urls')),
    path('api/', include('API.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
