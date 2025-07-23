from typing import List

import wdb_wallpaper.services.llm
from wdb_wallpaper.models.tag import Tag


def auto_generate_tags(image_file_path: str) -> List[Tag]:
    ai_tags = wdb_wallpaper.services.llm.generate_image_tags(
        provider='deepinfra',
        image_file_path=image_file_path
    )

    return [
        Tag.objects.get_or_create(name=tag)[0]
        for tag in ai_tags
    ] 