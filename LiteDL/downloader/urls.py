from django.urls import path
from . import views
from django.contrib.auth.decorators import user_passes_test
from .tasks import clean_old_downloads

urlpatterns = [
    path('', views.index, name='index'),
    path('download/', views.download, name='download'),
    path('clean/', user_passes_test(lambda u: u.is_superuser)(clean_old_downloads), name='clean'),
]