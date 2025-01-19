from django.core.management.base import BaseCommand

from wdb_wallpaper.models import Wallpaper

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        w = Wallpaper.objects.first()
        w.save()
        # self.stdout.write(self.style.SUCCESS('Successfully executed empty management command.'))
        from pprint import pprint as pp
        pp(w.__dict__)