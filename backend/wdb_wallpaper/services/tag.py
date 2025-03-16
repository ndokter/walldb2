from typing import List

import wdb_wallpaper.services.ollama_
from wdb_wallpaper.models.tag import Tag


def auto_generate_tags(image_file_path: str) -> List[Tag]:
    ollama_tags = wdb_wallpaper.services.ollama_.generate_image_tags(image_file_path=image_file_path)

    return [
        Tag.objects.get_or_create(name=ollama_tag, defaults={'auto_generated': True})[0]
        for ollama_tag in ollama_tags
    ] 