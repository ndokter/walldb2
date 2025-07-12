from django import forms


class WallpaperSearchForm(forms.Form):
    q = forms.CharField(
        label='Search',
        widget=forms.TextInput(
            attrs={'placeholder': 'Search wallpapers...',
                   'type': 'search'}),
        max_length=200,
        required=False
    )