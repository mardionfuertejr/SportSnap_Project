from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Count
from .models import Album
from .forms import AlbumForm
from dashboard.helpers import log_activity


class AlbumListView(generic.ListView):
    model = Album
    template_name = 'albums/album_list.html'
    context_object_name = 'albums'
    paginate_by = 9

    def get_queryset(self):
        qs = Album.objects.select_related('owner').annotate(
            num_photos=Count('photos')
        )

        # Non-staff users only see public albums + their own
        if not self.request.user.is_authenticated:
            qs = qs.filter(is_public=True)
        elif not self.request.user.is_staff:
            qs = qs.filter(Q(is_public=True) | Q(owner=self.request.user))

        query = self.request.GET.get('q', '').strip()
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(sport_category__icontains=query)
            )

        category = self.request.GET.get('category', '').strip()
        if category:
            qs = qs.filter(sport_category=category)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_query'] = self.request.GET.get('q', '')
        ctx['selected_category'] = self.request.GET.get('category', '')
        ctx['sport_categories'] = Album.SPORT_CATEGORIES
        return ctx


class AlbumDetailView(generic.DetailView):
    model = Album
    template_name = 'albums/album_detail.html'
    context_object_name = 'album'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        qs = Album.objects.select_related('owner')
        if not self.request.user.is_authenticated:
            qs = qs.filter(is_public=True)
        elif not self.request.user.is_staff:
            qs = qs.filter(Q(is_public=True) | Q(owner=self.request.user))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['photos'] = self.object.photos.select_related('uploaded_by').order_by('-uploaded_at')
        return ctx


class AlbumCreateView(LoginRequiredMixin, generic.CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/album_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        log_activity(self.request.user, 'created album', self.object.title)
        messages.success(self.request, f"Album '{self.object.title}' created!")
        return response

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = 'Create New Album'
        return ctx


class AlbumUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/album_form.html'
    slug_url_kwarg = 'slug'

    def test_func(self):
        album = self.get_object()
        return self.request.user == album.owner or self.request.user.is_staff

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Album '{self.object.title}' updated.")
        return response

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = 'Edit Album'
        return ctx


class AlbumDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Album
    template_name = 'albums/album_confirm_delete.html'
    success_url = reverse_lazy('albums:album_list')
    slug_url_kwarg = 'slug'

    def test_func(self):
        album = self.get_object()
        return self.request.user == album.owner or self.request.user.is_staff

    def form_valid(self, form):
        title = self.object.title
        log_activity(self.request.user, 'deleted album', title)
        response = super().form_valid(form)
        messages.success(self.request, f"Album '{title}' has been deleted.")
        return response
