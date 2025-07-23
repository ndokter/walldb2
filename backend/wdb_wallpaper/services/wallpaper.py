import io
import logging
import os

import wdb_wallpaper.services.chromadb
import wdb_wallpaper.services.llm
import wdb_wallpaper.services.tag
import wdb_wallpaper.services.thumbnail
import wdb_wallpaper.services.wallpaper
from django.core.files.images import ImageFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from django.db.models import Case, When
from PIL import Image
from wdb_wallpaper.models import Wallpaper
from wdb_wallpaper.tasks import (wallpaper_generate_description_task,
                                 wallpaper_generate_tags_task)

logger = logging.getLogger(__name__)


@transaction.atomic()
def create(image_file: ImageFile):
    """
    Create new Wallpaper and:
    - generate Thumbnail for it
    - generate AI tags
    - generate AI description (similar to tags)
    """
    wallpaper = Wallpaper.objects.create(image=image_file)
    wdb_wallpaper.services.thumbnail.create(wallpaper=wallpaper)
    
    logger.debug("Created %s", wallpaper)

    # Queue AI generated info tasks
    wallpaper_generate_tags_task.delay(wallpaper.id)
    wallpaper_generate_description_task.delay(wallpaper.id)

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


def search_by_ai_description(query, max_results=50):
    wallpaper_id_keys = wdb_wallpaper.services.chromadb.search(query, max_results=max_results)

    # Sort the queryset using the chromadb result keys because they indicate relevance
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(wallpaper_id_keys)])
    wallpapers = Wallpaper.objects.filter(pk__in=wallpaper_id_keys).order_by(preserved)
    
    return wallpapers


def set_ai_generated_tags(wallpaper):
    tags = wdb_wallpaper.services.tag.auto_generate_tags(image_file_path=wallpaper.image.path)
    
    wallpaper.tags.add(*tags)

    logger.info("Saved auto generated tags '%s' for wallpaper %s", tags, wallpaper)


def set_ai_generated_description(wallpaper):
    wallpaper_description = wdb_wallpaper.services.llm.generate_description(
        provider='deepinfra',
        image_file_path=wallpaper.image.path
    )

    wdb_wallpaper.services.chromadb.add_description(
        key=str(wallpaper.id), 
        description=wallpaper_description
    )

    wallpaper.chromadb_description = wallpaper_description
    wallpaper.save(update_fields=['chromadb_description'])

    logger.info("Saved auto generated description for wallpaper %s", wallpaper)
