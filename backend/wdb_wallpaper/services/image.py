import hashlib
import math
from io import BytesIO

from PIL import Image
from django.core.files.images import ImageFile

from wdb_wallpaper.services.exceptions import UnsupportedFileExtensionError


def get_format(image_file: ImageFile) -> str:
    """ File format e.g. JPEG, PNG """
    return Image.open(image_file).format


def calculate_aspect_ratio(width: int, height: int) -> str:
    gcd = math.gcd(width, height)
    simplified_width = width // gcd
    simplified_height = height // gcd
    return f'{simplified_width}:{simplified_height}'  # e.g. '16:9'


def calculate_md5_hash(image_file: ImageFile) -> str:
    md5hash = hashlib.md5(Image.open(image_file).tobytes())
    return md5hash.hexdigest()


def generate_thumbnail(image_file: ImageFile, width=300, height=200) -> bytes:
    file_format = get_format(image_file=image_file)
    if file_format not in ('JPEG', 'PNG'):
        raise UnsupportedFileExtensionError(
            'File extension: \'{extension}\' not supported for thumbnail',
            file_format
        )

    img = Image.open(image_file)

    src_width, src_height = img.size
    src_ratio = float(src_width) / float(src_height)
    dst_width, dst_height = width, height
    dst_ratio = float(dst_width) / float(dst_height)

    if dst_ratio < src_ratio:
        crop_height = src_height
        crop_width = crop_height * dst_ratio
        x_offset = int(float(src_width - crop_width) / 2)
        y_offset = 0
    else:
        crop_width = src_width
        crop_height = crop_width / dst_ratio
        x_offset = 0
        y_offset = int(float(src_height - crop_height) / 3)

    img = img.crop((x_offset,
                    y_offset,
                    x_offset+int(crop_width),
                    y_offset+int(crop_height)))

    img = img.resize((int(dst_width), int(dst_height)), Image.LANCZOS)

    temp_handle = BytesIO()

    img.save(temp_handle, file_format, quality=90)

    temp_handle.seek(0)

    image_bytes = temp_handle.read()

    temp_handle.close()
    img.close()
    image_file.close()

    return image_bytes