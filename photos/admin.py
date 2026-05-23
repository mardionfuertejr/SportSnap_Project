from django.contrib import admin
from .models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'album', 'uploaded_by', 'sport_tag', 'uploaded_at')
    list_filter = ('sport_tag', 'uploaded_at')
    search_fields = ('caption', 'album__title', 'uploaded_by__username')
