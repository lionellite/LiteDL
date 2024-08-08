import yt_dlp
from django.shortcuts import render, redirect
from .models import VideoDownload

def home(request):
    if request.method == 'POST':
        url = request.POST['url']
        try:
            ydl_opts = {}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', url)
                file_path = ydl.prepare_filename(info)
                ydl.download([url])
            video_download = VideoDownload(url=url, video_title=video_title, downloaded_file=file_path)
            video_download.save()
            return redirect('download_list')
        except Exception as e:
            error_message = f"Une erreur s'est produite lors du téléchargement : {e}"
            return render(request, 'home.html', {'error_message': error_message})
    return render(request, 'home.html')

def download_list(request):
    downloads = VideoDownload.objects.all()
    return render(request, 'download_list.html', {'downloads': downloads})