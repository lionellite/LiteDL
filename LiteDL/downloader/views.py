import os
import time
from django.shortcuts import render
from django.http import FileResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.conf import settings
import yt_dlp

ALLOWED_DOMAINS = ['youtube.com', 'youtu.be', 'facebook.com', 'fb.watch', 'tiktok.com']


@require_http_methods(["GET"])
def index(request):
    return render(request, 'downloader/index.html')


@require_http_methods(["POST"])
def download(request):
    url = request.POST.get('url', '').strip()

    if not url or not any(domain in url for domain in ALLOWED_DOMAINS):
        return render(request, 'downloader/index.html', {'message': 'URL invalide ou non supportée.'})

    try:
        ydl_opts = {
            'outtmpl': os.path.join(settings.MEDIA_ROOT, '%(title)s.%(ext)s'),
            'format': 'best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Vérifier si le fichier existe et est accessible
        if not os.path.exists(filename) or not os.access(filename, os.R_OK):
            raise FileNotFoundError("Le fichier téléchargé n'est pas accessible.")

        # Configurer la réponse pour le téléchargement
        response = FileResponse(open(filename, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(filename)}"'

        # Programmer la suppression du fichier
        default_storage.delete(filename)

        return response

    except yt_dlp.utils.DownloadError as e:
        message = f"Erreur lors du téléchargement : {str(e)}"
    except FileNotFoundError as e:
        message = str(e)
    except Exception as e:
        message = f"Une erreur inattendue s'est produite : {str(e)}"

    return render(request, 'downloader/index.html', {'message': message})