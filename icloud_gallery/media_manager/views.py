from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage

from pyicloud import PyiCloudService

from .forms import ICloudLoginForm, TwoFactorForm
from .models import Media
from .services.icloud_client import iCloudClient


def icloud_login_view(request):
    if request.method == 'POST':
        form = ICloudLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            api = PyiCloudService(email, password)

            if api.requires_2fa:
                request.session['icloud_email'] = email
                request.session['icloud_password'] = password
                return redirect('icloud_2fa')
            elif api.requires_2sa:
                messages.error(request, "İki aşamalı kimlik doğrulama desteklenmiyor.")
            elif api.is_trusted_session:
                request.session['icloud_authenticated'] = True
                request.session['icloud_email'] = email
                request.session['icloud_password'] = password
                return redirect('gallery')
            else:
                messages.error(request, "Oturum açılamadı.")
    else:
        form = ICloudLoginForm()
    return render(request, 'icloud_login.html', {'form': form})


def icloud_2fa_view(request):
    if request.method == 'POST':
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            email = request.session.get('icloud_email')
            password = request.session.get('icloud_password')
            api = PyiCloudService(email, password)

            if api.requires_2fa:
                if api.validate_2fa_code(code):
                    if not api.is_trusted_session:
                        api.trust_session()
                    request.session['icloud_authenticated'] = True
                    return redirect('gallery')
                else:
                    messages.error(request, "Kod yanlış.")
    else:
        form = TwoFactorForm()
    return render(request, 'icloud_2fa.html', {'form': form})


@login_required
def gallery_view(request):
    if not request.session.get('icloud_authenticated'):
        return redirect('icloud_login')

    email = request.session.get('icloud_email')
    password = request.session.get('icloud_password')
    api = PyiCloudService(email, password)

    media_items = []

    try:
        photos = api.photos.all
        for photo in photos:
            try:
                media_items.append({
                    'id': photo.asset_id,
                    'url': photo.download().url,
                    'type': 'photo'
                })
            except Exception:
                continue
    except Exception as e:
        print("Fotoğraflar alınamadı:", e)

    try:
        videos = api.photos.videos
        for video in videos:
            try:
                media_items.append({
                    'id': video.asset_id,
                    'url': video.download().url,
                    'type': 'video'
                })
            except Exception:
                continue
    except Exception as e:
        print("Videolar alınamadı:", e)

    return render(request, 'gallery.html', {'media_items': media_items})




@require_POST
@login_required
def upload_media(request):
    file = request.FILES.get('file')
    if not file:
        return JsonResponse({'status': 'error', 'message': 'Dosya bulunamadı.'}, status=400)

    file_path = default_storage.save(file.name, file)

    email = request.session.get('icloud_email')
    password = request.session.get('icloud_password')
    client = iCloudClient(email, password)

    try:
        with default_storage.open(file_path, 'rb') as f:
            client.upload_media(f)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'success'})


@require_POST
@login_required
def delete_selected_media(request):
    ids = request.POST.getlist('media_ids[]')
    if not ids:
        return JsonResponse({'status': 'error', 'message': 'Silinecek medya seçilmedi.'}, status=400)

    email = request.session.get('icloud_email')
    password = request.session.get('icloud_password')
    client = iCloudClient(email, password)

    try:
        client.delete_media(ids)
        Media.objects.filter(user=request.user, icloud_id__in=ids).delete()
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'success'})
