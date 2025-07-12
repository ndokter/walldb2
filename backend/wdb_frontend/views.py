import wdb_wallpaper.services.wallpaper
from django.db.models import Q
from django.views.generic.list import ListView
from wdb_frontend.forms import WallpaperSearchForm
from wdb_wallpaper.models.wallpaper import Wallpaper


class IndexView(ListView):
    model = Wallpaper
    paginate_by = 30
    template_name = 'wdb_frontend/index.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.search_form = WallpaperSearchForm(self.request.GET)
        if self.search_form.is_valid():
            if q := self.search_form.cleaned_data['q']:
                queryset = wdb_wallpaper.services.wallpaper.search_by_ai_description(q)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = WallpaperSearchForm(self.request.GET)
        return context