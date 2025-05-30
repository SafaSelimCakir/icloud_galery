from django.urls import path
from .views import gallery_view, upload_media, delete_selected_media,icloud_login_view
from . import views


urlpatterns = [
    path('', gallery_view, name='gallery'),
    path('upload/', upload_media, name='upload_media'),
    path('delete/', delete_selected_media, name='delete_selected_media'),
    path("login/", icloud_login_view, name="icloud_login"),
    path('icloud/login/', views.icloud_login_view, name='icloud_login'),
    path('icloud/2fa/', views.icloud_2fa_view, name='icloud_2fa'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('gallery/', gallery_view, name='gallery'),

]

