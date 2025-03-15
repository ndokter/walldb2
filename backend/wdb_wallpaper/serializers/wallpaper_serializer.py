from rest_framework import serializers

from wdb_wallpaper.models.wallpaper import Wallpaper


class WallpaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallpaper
        fields = ['id', 'image', 'image_size', 'width', 'height', 'aspect_ratio', 'hash', 'tags']