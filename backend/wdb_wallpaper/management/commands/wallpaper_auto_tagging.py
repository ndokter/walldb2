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
        untagged_wallpapers = Wallpaper.objects.filter(tags__isnull=True)

        logger.info("Starting with auto tagging")

        for wallpaper in untagged_wallpapers:
            wdb_wallpaper.services.wallpaper.auto_generate_tags(wallpaper=wallpaper)