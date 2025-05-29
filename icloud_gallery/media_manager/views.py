from django.shortcuts import render, redirect
from .models import Media
from .services.sync import sync_media
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.conf import settings
from django.http import JsonResponse
from .services.icloud_client import iCloudClient

def gallery_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Kullanıcının verileri çekilmişse kullan, çekilmemişse senkronize et
    if Media.objects.filter(user=request.user).count() == 0:
        sync_media(request.user)

    media = Media.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'media_manager/gallery.html', {'media': media})


@require_POST
def upload_media(request):
    file = request.FILES.get('file')
    if not file:
        return JsonResponse({'status': 'error', 'message': 'Dosya bulunamadı.'}, status=400)

    # Geçici olarak dosyayı kaydet
    file_path = default_storage.save(file.name, file)

    # iCloud’a yükle
    username = request.user.email
    password = request.user.icloud_password  # HATALI OLAN SATIR DÜZELTİLDİ
    client = iCloudClient(username, password)

    with default_storage.open(file_path, 'rb') as f:
        client.upload_media(f)

    return JsonResponse({'status': 'success'})


@require_POST
def delete_selected_media(request):
    ids = request.POST.getlist('media_ids[]')
    if not ids:
        return JsonResponse({'status': 'error', 'message': 'Silinecek medya seçilmedi.'}, status=400)

    username = request.user.email
    password = request.user.icloud_password  # HATALI OLAN SATIR DÜZELTİLDİ
    client = iCloudClient(username, password)

    client.delete_media(ids)
    Media.objects.filter(user=request.user, icloud_id__in=ids).delete()

    return JsonResponse({'status': 'success'})
