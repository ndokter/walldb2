import io
import logging
import os

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
    """ Create new Wallpaper and generate Thumbnail for it """

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


def auto_generate_tags(wallpaper):
    tags = wdb_wallpaper.services.tag.auto_generate_tags(image_file_path=wallpaper.image.path)
    
    wallpaper.tags.add(*tags)
    wallpaper.save()

    logger.info('Saved auto generated %s for wallpaper %s', tags, wallpaper)