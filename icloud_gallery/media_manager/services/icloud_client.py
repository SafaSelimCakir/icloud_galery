from pyicloud import PyiCloudService
import datetime
import mimetypes

class iCloudClient:
    def upload_media(self, file_obj):
        # pyicloud doğrudan yükleme desteklemez, bunun için API ters mühendislik gerekir
        # Ancak şimdilik mock fonksiyon gibi yapalım:
        print("Mock upload: iCloud API ile gerçek yükleme işlemi burada olacak.")

    def delete_media(self, ids):
        # pyicloud yine doğrudan silme desteklemiyor
        # Ancak örnek:
        for photo in self.api.photos.all:
            if photo.id in ids:
                photo.delete()

    def __init__(self, username, password):
        self.api = PyiCloudService(username, password)
        if self.api.requires_2fa:
            print("2FA kodunu girin:")
            code = input("Kod: ")
            self.api.validate_2fa_code(code)
            if not self.api.is_trusted_session:
                print("Güvenli oturum başarısız")

    def fetch_all_media(self):
        items = self.api.photos.all
        media = []
        for item in items:
            created = datetime.datetime.fromtimestamp(item.created.timestamp())
            media.append({
                'id': item.id,
                'filename': item.filename,
                'type': 'video' if item.uti.startswith('public.movie') else 'photo',
                'created_at': created,
                'thumbnail_url': item.thumbnail_url,
                'full_url': item.asset_url,
            })
        return media
