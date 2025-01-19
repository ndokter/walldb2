from django.db import models


class Thumbnail(models.Model):
    wallpaper = models.OneToOneField('Wallpaper',  related_name='thumbnail',  on_delete=models.CASCADE)

    image = models.ImageField(upload_to='thumbnails', blank=True)
    width = models.IntegerField()
    height = models.IntegerField()   

    def save(self, **kwargs):
        self.width, self.height = self.image.width, self.image.height
        self.image.name = f't_{self.wallpaper.hash}.{self.wallpaper.image_format.lower()}'

        return super().save(**kwargs)