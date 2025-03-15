import wdb_wallpaper.services.image
from django.db import models


class Wallpaper(models.Model):
    tags = models.ManyToManyField('Tag', blank=True)

    image = models.ImageField(upload_to='wallpapers', null=True)
    image_format = models.CharField(max_length=4, help_text='e.g. png', blank=True)
    image_size = models.IntegerField(help_text='size in bytes', blank=True)
    width = models.IntegerField(blank=True)
    height = models.IntegerField(blank=True)
    aspect_ratio = models.CharField(max_length=6, help_text='e.g. 16:9', blank=True)
    hash = models.CharField(unique=True, max_length=32, blank=True)

    chromadb_description = models.TextField(
        help_text="Description of image to make searchable with ChromaDB", 
        null=True, 
        blank=True)
    chromadb_description_added = models.BooleanField(
        default=False, 
        help_text="If added to ChromaDB")

    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'<Wallpaper {self.image.name}>'

    def save(self, **kwargs):
        # Precalculate properties based on 'image'. Used for filtering etc.
        self.hash = wdb_wallpaper.services.image.calculate_md5_hash(image_file=self.image)
        self.width, self.height = self.image.width, self.image.height
        self.aspect_ratio = wdb_wallpaper.services.image.calculate_aspect_ratio(
            width=self.width, 
            height=self.height)
        self.image_size = self.image.size
        self.image_format = wdb_wallpaper.services.image.get_format(image_file=self.image)
        self.image.name = f'w_{self.hash}.{self.image_format.lower()}'

        return super().save(**kwargs)