from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction


class WallpaperSearchForm(forms.Form):
    q = forms.CharField(
        label='Search',
        widget=forms.TextInput(
            attrs={'placeholder': 'Search wallpapers...',
                   'type': 'search'}),
        max_length=200,
        required=False
    )


class LoginForm(forms.Form):
    email = forms.CharField(max_length=254, label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean_email(self):
        return self.cleaned_data['email'].lower()

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            cleaned_data['user'] = authenticate(username=email, password=password)

        if not cleaned_data.get('user'):
            raise forms.ValidationError('Invalid login credentials.')

        return cleaned_data


class RegisterForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password_confirmation = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
        help_text='Enter the same password as above, for verification.'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "The email address '{}' is already registered".format(email)
            )

        return email.lower()

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            raise forms.ValidationError(
                "The two password fields didn't match."
            )

    @transaction.atomic
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()

        return user