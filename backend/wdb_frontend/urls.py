from django.contrib.auth import views as auth_views
from django.urls import include, path
from wdb_frontend.views.user import (UserLoginView, UserLogoutView,
                                     UserRegisterView)
from wdb_frontend.views.wallpaper import WallpaperListView, WallpaperDetailView

user_patterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]


urlpatterns = [
    path('', WallpaperListView.as_view(), name="index"),
    path('wallpaper/<str:hash>/', WallpaperDetailView.as_view(), name='wallpaper-detail'),
    path('user/', include((user_patterns, 'user'), namespace='user')),
]
