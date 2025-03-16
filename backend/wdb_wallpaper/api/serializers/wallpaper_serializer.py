from rest_framework import serializers
from wdb_wallpaper.models.wallpaper import Wallpaper

from .tag_serializer import TagSerializer


class WallpaperSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Wallpaper
        fields = ['id', 'image', 'image_size', 'width', 'height', 'aspect_ratio', 'tags', 'chromadb_description']