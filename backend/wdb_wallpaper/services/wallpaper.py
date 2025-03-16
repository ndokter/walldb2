import io
import logging
import os

import wdb_wallpaper.services.chromadb
import wdb_wallpaper.services.ollama_
import wdb_wallpaper.services.tag
import wdb_wallpaper.services.thumbnail
import wdb_wallpaper.services.wallpaper
from django.core.files.images import ImageFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from PIL import Image
from wdb_wallpaper.models import Wallpaper

logger = logging.getLogger(__name__)


@transaction.atomic()
def create(image_file: ImageFile):
    """
    Create new Wallpaper and generate Thumbnail for it
    
    Note: does not generate ai tags and descriptions. These are done 
    occassionally using a stronger machine running ollama
    """
    
    wallpaper = Wallpaper.objects.create(image=image_file)
    wdb_wallpaper.services.thumbnail.create(wallpaper=wallpaper)
    
    logger.debug("Created %s", wallpaper)
    
    return wallpaper


def update(wallpaper):
    wallpaper.save()

    return wallpaper


def import_file(full_path: str):
    with Image.open(full_path) as img:
        img_bytes_array = io.BytesIO()
        img.save(img_bytes_array, format=img.format)
        img_bytes = img_bytes_array.getvalue()

    simple_file = SimpleUploadedFile(
        name=os.path.basename(full_path),
        content=img_bytes,
        content_type=img.format
    )

    create(image_file=simple_file)


def set_ai_generated_tags(wallpaper):
    tags = wdb_wallpaper.services.tag.auto_generate_tags(image_file_path=wallpaper.image.path)
    
    wallpaper.tags.add(*tags)
    wallpaper.save()

    logger.info("Saved auto generated tags '%s' for wallpaper %s", tags, wallpaper)


def set_ai_generated_description(wallpaper):
    wallpaper_description = wdb_wallpaper.services.ollama_.generate_description(
        image_file_path=wallpaper.image.path
    )

    wdb_wallpaper.services.chromadb.add_description(
        key=str(wallpaper.id), 
        description=wallpaper_description
    )

    wallpaper.chromadb_description = wallpaper_description
    wallpaper.save()

    logger.info("Saved auto generated description for wallpaper %s", wallpaper)
