from django.urls import path
from .views import gallery_view, upload_media, delete_selected_media

urlpatterns = [
    path('', gallery_view, name='gallery'),
    path('upload/', upload_media, name='upload_media'),
    path('delete/', delete_selected_media, name='delete_selected_media'),
]

