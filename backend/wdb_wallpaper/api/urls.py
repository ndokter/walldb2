from django.urls import path

from .views import WallpaperListAPIView

urlpatterns = [
    path('wallpapers/', WallpaperListAPIView.as_view())
]