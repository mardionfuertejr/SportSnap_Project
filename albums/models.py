from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
import itertools


class Album(models.Model):
    SPORT_CATEGORIES = [
        ('football', 'Football'),
        ('basketball', 'Basketball'),
        ('soccer', 'Soccer'),
        ('baseball', 'Baseball'),
        ('tennis', 'Tennis'),
        ('swimming', 'Swimming'),
        ('athletics', 'Athletics'),
        ('volleyball', 'Volleyball'),
        ('hockey', 'Hockey'),
        ('boxing', 'Boxing'),
        ('cycling', 'Cycling'),
        ('motorsport', 'Motorsport'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    sport_category = models.CharField(max_length=30, choices=SPORT_CATEGORIES, default='other')
    cover_image = CloudinaryField('cover', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = base_slug
            for i in itertools.count(1):
                if not Album.objects.filter(slug=self.slug).exists():
                    break
                self.slug = f"{base_slug}-{i}"
        super().save(*args, **kwargs)

    @property
    def photo_count(self):
        return self.photos.count()

    @property
    def cover_url(self):
        if self.cover_image:
            return self.cover_image.url
        return None

    def get_absolute_url(self):
        return reverse('albums:album_detail', kwargs={'slug': self.slug})
