from django.core.files.images import ImageFile
from django.core.files.uploadedfile import SimpleUploadedFile

from wdb_wallpaper.models.wallpaper import Wallpaper
import wdb_wallpaper.services.image
from wdb_wallpaper.models.thumbnail import Thumbnail


def create(wallpaper: Wallpaper, width=300, height=200) -> Thumbnail:
    """ Create new Thumbnail based on Wallpaper """
    thumbnail = Thumbnail(
        wallpaper=wallpaper,
        width=width, 
        height=height)
  
    image = wdb_wallpaper.services.image.generate_thumbnail(
        image_file=wallpaper.image, 
        width=width, 
        height=height)

    thumbnail.image = SimpleUploadedFile(
        name=f't_{wallpaper.hash}.{wallpaper.image_format.lower()}',
        content=image,
        content_type=wallpaper.image_format)

    thumbnail.save()

    return thumbnail
