from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from albums.models import Album
from photos.models import Photo
from .models import ActivityLog


class DashboardView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    template_name = 'dashboard/dashboard.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['total_users'] = User.objects.count()
        ctx['total_albums'] = Album.objects.count()
        ctx['total_photos'] = Photo.objects.count()
        ctx['recent_activity'] = ActivityLog.objects.select_related('user')[:25]
        ctx['recent_users'] = User.objects.order_by('-date_joined')[:5]
        ctx['recent_albums'] = Album.objects.select_related('owner')[:5]
        return ctx
