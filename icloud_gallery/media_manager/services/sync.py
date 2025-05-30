from .icloud_client import iCloudClient
from media_manager.models import Media
from django.contrib.auth import get_user_model

def sync_media(user):
    username = user.icloud_email
    password = user.icloud_password
    client = iCloudClient(username, password)
    media_list = client.fetch_all_media()

    client = iCloudClient(username, password)
    media_list = client.fetch_all_media()

    for media_data in media_list:
        Media.objects.update_or_create(
            icloud_id=media_data['id'],
            defaults={
                'user': user,
                'file_name': media_data['filename'],
                'file_type': media_data['type'],
                'created_at': media_data['created_at'],
                'thumbnail_url': media_data['thumbnail_url'],
                'full_url': media_data['full_url'],
            }
        )
