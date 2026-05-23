from django.contrib import admin
from .models import Album


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'sport_category', 'is_public', 'created_at')
    list_filter = ('sport_category', 'is_public', 'created_at')
    search_fields = ('title', 'description', 'owner__username')
    prepopulated_fields = {'slug': ('title',)}
