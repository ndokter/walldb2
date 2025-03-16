import wdb_wallpaper.services.chromadb
import wdb_wallpaper.services.wallpaper
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

from ..models import Wallpaper
from .serializers import WallpaperSerializer


class WallpaperListAPIView(generics.ListAPIView):
    queryset = Wallpaper.objects.all()
    serializer_class = WallpaperSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]#, filters.OrderingFilter]
    filterset_fields = ['width', 'height', 'aspect_ratio']
    ordering_fields = ['width', 'height', 'aspect_ratio']
    search_fields = ['tags__name']
    ordering = ['pk']

    def get_queryset(self):
        q = self.request.query_params.get('q')
        if q is not None:
            return wdb_wallpaper.services.wallpaper.search_by_ai_description(q)

        return super().get_queryset()