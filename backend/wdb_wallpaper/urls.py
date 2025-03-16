from django.urls import include, path

urlpatterns = [
    path('api/', include('wdb_wallpaper.api.urls')),
]