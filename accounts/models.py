from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    SPORT_CHOICES = [
        ('football', 'Football'),
        ('basketball', 'Basketball'),
        ('soccer', 'Soccer'),
        ('baseball', 'Baseball'),
        ('tennis', 'Tennis'),
        ('swimming', 'Swimming'),
        ('athletics', 'Athletics'),
        ('volleyball', 'Volleyball'),
        ('hockey', 'Hockey'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = CloudinaryField('avatar', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    favorite_sport = models.CharField(max_length=30, choices=SPORT_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return 'https://ui-avatars.com/api/?name={}&background=0d6efd&color=fff&size=128'.format(self.user.username)
