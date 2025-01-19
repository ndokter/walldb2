import hashlib
import io

from django.db import transaction

import wdb_wallpaper.services.thumbnail
from wdb_wallpaper.models import Wallpaper


@transaction.atomic()
def create(image_file):
    """ Create new Wallpaper and generate Thumbnail for it """

    wallpaper = Wallpaper.objects.create(image=image_file)
    
    wdb_wallpaper.services.thumbnail.create(wallpaper=wallpaper)

    return wallpaper


def update(wallpaper):
    wallpaper.save()

    return wallpaper