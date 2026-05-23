from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from albums.models import Album


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    image = CloudinaryField('photo')
    caption = models.CharField(max_length=300, blank=True)
    sport_tag = models.CharField(max_length=50, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.caption or f"Photo #{self.pk}"

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return ''
