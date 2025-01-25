from django.contrib import admin

from wdb_wallpaper.models.thumbnail import Thumbnail
from wdb_wallpaper.models.tag import Tag
from wdb_wallpaper.models import Wallpaper
import wdb_wallpaper.services.wallpaper


class WallpaperAdmin(admin.ModelAdmin):
    exclude = ('tags',)

    def save_model(self, request, obj, form, change):
        if change:
            wdb_wallpaper.services.wallpaper.update(wallpaper=obj)
        else:
            wdb_wallpaper.services.wallpaper.create(image_file=form.cleaned_data['image'])


class ThumbnailAdmin(admin.ModelAdmin):
    pass


class TagAdmin(admin.ModelAdmin):
    pass


admin.site.register(Wallpaper, WallpaperAdmin)
admin.site.register(Thumbnail, ThumbnailAdmin)
admin.site.register(Tag, TagAdmin)