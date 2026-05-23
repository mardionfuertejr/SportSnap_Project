from django import forms
from .models import Photo


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class PhotoUploadForm(forms.Form):
    """Handles multiple file uploads in a single form submission."""
    images = forms.FileField(
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'multiple': True,
            'accept': 'image/*',
        }),
        label='Select Photos',
    )
    caption = forms.CharField(
        max_length=300,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Optional caption for all photos',
        }),
    )
    sport_tag = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., goal, slam-dunk',
        }),
    )


class PhotoEditForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['caption', 'sport_tag']
        widgets = {
            'caption': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Update caption...',
            }),
            'sport_tag': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., goal, slam-dunk',
            }),
        }
