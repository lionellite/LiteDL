from django.db import models

class VideoDownload(models.Model):
    url = models.URLField()
    video_title = models.CharField(max_length=200)
    downloaded_file = models.FileField(upload_to='downloads/')
    download_date = models.DateTimeField(auto_now_add=True)
