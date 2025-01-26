import os

import wdb_wallpaper.services.wallpaper
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Read folder from disk and import all images into Wallpaper model.

    Duplicate files will fail on unique file hash constraint.
    """

    def add_arguments(self, parser):
        parser.add_argument('source_folder', type=str, help='Folder containing wallpapers to import')

    def handle(self, *args, **kwargs):
        source_folder = kwargs['source_folder']

        for folder_path, _, file_names in os.walk(source_folder):
            for file_name in file_names:
                full_path = os.path.join(folder_path, file_name)

                try:
                    wdb_wallpaper.services.wallpaper.import_file(full_path)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error reading file {full_path}: {e}')) 
