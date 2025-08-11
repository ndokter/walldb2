import wdb_wallpaper.services.wallpaper
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from wdb_frontend.forms import WallpaperSearchForm
from wdb_wallpaper.models.wallpaper import Wallpaper


class SearchMixin:
    """ Add WallpaperSearchForm to views """
    def get_queryset(self):
        queryset = super().get_queryset()
        self.search_form = WallpaperSearchForm(self.request.GET)
        if self.search_form.is_valid():
            if q := self.search_form.cleaned_data['q']:
                queryset = wdb_wallpaper.services.wallpaper.search_by_ai_description(q)
        return queryset


class IndexView(ListView):
    model = Wallpaper
    paginate_by = 100
    template_name = 'wdb_frontend/wallpaper_list.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.search_form = WallpaperSearchForm(self.request.GET)
        if self.search_form.is_valid():
            if q := self.search_form.cleaned_data['q']:
                queryset = wdb_wallpaper.services.wallpaper.search_by_ai_description(q)
        return queryset


class WallpaperDetailView(DetailView):
    model = Wallpaper
    template_name = 'wdb_frontend/wallpaper_detail.html'
    slug_field = 'hash'
    slug_url_kwarg = 'hash'