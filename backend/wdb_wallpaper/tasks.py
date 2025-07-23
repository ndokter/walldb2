# wdb_wallpaper/tasks.py
import logging

from celery import shared_task

from .models import Wallpaper

logger = logging.getLogger(__name__)


@shared_task
def wallpaper_generate_description_task(wallpaper_id):
    import wdb_wallpaper.services.wallpaper
    
    wallpaper = Wallpaper.objects.get(id=wallpaper_id)

    wdb_wallpaper.services.wallpaper.set_ai_generated_description(wallpaper=wallpaper)


@shared_task
def wallpaper_generate_tags_task(wallpaper_id):
    import wdb_wallpaper.services.wallpaper
    
    wallpaper = Wallpaper.objects.get(id=wallpaper_id)

    wdb_wallpaper.services.wallpaper.set_ai_generated_tags(wallpaper=wallpaper)