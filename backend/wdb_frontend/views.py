from django.views.generic.list import ListView
from wdb_wallpaper.models.wallpaper import Wallpaper


class IndexView(ListView):
    model = Wallpaper
    paginate_by = 30
    template_name = 'wdb_frontend/index.html'