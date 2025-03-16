import logging

import wdb_wallpaper.services.wallpaper
from django.core.management.base import BaseCommand
from wdb_wallpaper.models.wallpaper import Wallpaper

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Use ollama to generate tags/labels for all Wallpaper's that don't have any tags yet.
    """
    def handle(self, *args, **kwargs):
        wallpapers_without_description = Wallpaper.objects.filter(chromadb_description__isnull=True)

        logger.info("Starting with auto descriptions")

        for wallpaper in wallpapers_without_description:
            wdb_wallpaper.services.wallpaper.set_ai_generated_description(wallpaper=wallpaper)