from django.db import models
from django.conf import settings

class Media(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    icloud_id = models.CharField(max_length=255, unique=True)  # iCloud'daki ID
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10, choices=[('photo', 'Photo'), ('video', 'Video')])
    created_at = models.DateTimeField()
    thumbnail_url = models.URLField(blank=True, null=True)
    full_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.file_name} ({self.file_type})"
