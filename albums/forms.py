from django import forms
from .models import Album


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description', 'sport_category', 'cover_image', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Championship Finals 2025',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe this album...',
            }),
            'sport_category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
