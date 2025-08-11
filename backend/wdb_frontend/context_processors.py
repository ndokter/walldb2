from wdb_frontend.forms import WallpaperSearchForm


def search_context(request):
    return {
        'search_form': WallpaperSearchForm(request.GET)
    }