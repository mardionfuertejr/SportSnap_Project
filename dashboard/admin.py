from django.contrib import admin
from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'target', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'action', 'target')
    readonly_fields = ('user', 'action', 'target', 'timestamp')
