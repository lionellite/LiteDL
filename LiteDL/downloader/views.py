import os
from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
#from ratelimit.decorators import ratelimit
import yt_dlp


def truncate_filename(filename, max_length=100):
    name, ext = os.path.splitext(filename)
    if len(name) > max_length:
        return name[:max_length] + '...' + ext
    return filename


@require_http_methods(["GET"])
def index(request):
    return render(request, 'downloader/index.html')


@require_http_methods(["POST"])
#@ratelimit(key='ip', rate='10/h', block=True)
def get_video_info(request):
    url = request.POST.get('url', 'get_video_info/').strip()

    if not url:
        return JsonResponse({'error': 'URL invalide.'}, status=400)

    try:
        ydl_opts = {'format': 'bestaudio/best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = [
            {
                'format_id': f['format_id'],
                'ext': f['ext'],
                'resolution': f.get('resolution', 'Audio'),
                'filesize': f.get('filesize', 'Unknown')
            }
            for f in info['formats'] if f.get('resolution') != 'audio only'
        ]

        return JsonResponse({
            'title': truncate_filename(info['title']),
            'thumbnail': info['thumbnail'],
            'formats': formats
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(["POST"])
#@ratelimit(key='ip', rate='5/h', block=True)
def download(request):
    url = request.POST.get('url', '').strip()
    format_id = request.POST.get('format_id', '').strip()

    if not url or not format_id:
        return JsonResponse({'error': 'URL ou format invalide.'}, status=400)

    try:
        ydl_opts = {
            'format': format_id,
            'outtmpl': os.path.join(settings.MEDIA_ROOT, '%(title)s.%(ext)s'),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            truncated_filename = truncate_filename(os.path.basename(filename))

        response = FileResponse(open(filename, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{truncated_filename}"'
        return response

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)