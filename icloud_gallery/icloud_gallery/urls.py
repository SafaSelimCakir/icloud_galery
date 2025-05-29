from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('media_manager.urls')),
    path('', include('users.urls')),
]
