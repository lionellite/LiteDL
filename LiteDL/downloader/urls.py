from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_video_info/', views.get_video_info, name='get_video_info'),
    path('download/', views.download, name='download'),
]