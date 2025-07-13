from django.urls import path

from .views import IndexView, WallpaperDetailView

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('wallpaper/<str:hash>/', WallpaperDetailView.as_view(), name='wallpaper-detail')
]