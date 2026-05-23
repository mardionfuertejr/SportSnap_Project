from django import forms
from .models import Photo, Album

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E.g., Summer Olympics 2024'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'description', 'image', 'album']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E.g., Championship Game'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'album': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PhotoForm, self).__init__(*args, **kwargs)
        if user and not user.is_superuser:
            self.fields['album'].queryset = Album.objects.filter(owner=user)
        elif user and user.is_superuser:
            self.fields['album'].queryset = Album.objects.all()