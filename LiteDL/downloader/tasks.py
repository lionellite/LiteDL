import os
import time
from django.conf import settings

def clean_old_downloads():
    now = time.time()
    media_root = settings.MEDIA_ROOT
    for filename in os.listdir(media_root):
        file_path = os.path.join(media_root, filename)
        if os.path.isfile(file_path):
            if os.stat(file_path).st_mtime < now - settings.DOWNLOAD_EXPIRY:
                os.remove(file_path)