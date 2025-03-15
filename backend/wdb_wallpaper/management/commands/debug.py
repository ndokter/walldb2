from django.core.management.base import BaseCommand

from wdb_wallpaper.models import Wallpaper

import wdb_wallpaper.services.ollama_

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        w = Wallpaper.objects.first()

        wdb_wallpaper.services.ollama_.generate_description(image_file_path=w.image.path)