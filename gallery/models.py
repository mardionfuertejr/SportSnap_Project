from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User

class Album(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Photo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = CloudinaryField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title