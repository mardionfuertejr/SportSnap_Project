from django.db import models
from django.contrib.auth.models import User


class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='activity_logs')
    action = models.CharField(max_length=100)
    target = models.CharField(max_length=200, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} — {self.action} {self.target}"
