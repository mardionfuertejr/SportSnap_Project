from .models import ActivityLog


def log_activity(user, action, target=''):
    """Convenience function to record a user action."""
    ActivityLog.objects.create(user=user, action=action, target=target)
