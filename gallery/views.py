from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Album, Photo
from .forms import AlbumForm, PhotoForm
from django.db.models import Q
import cloudinary.uploader

class IsOwnerOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_superuser or obj.owner == self.request.user

class AlbumListView(ListView):
    model = Album
    template_name = 'gallery/home.html'
    context_object_name = 'albums'
    paginate_by = 6
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Album.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            ).order_by('-created_at')
        return Album.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class DashboardView(LoginRequiredMixin, ListView):
    model = Album
    template_name = 'gallery/dashboard.html'
    context_object_name = 'albums'
    paginate_by = 6
    
    def get_queryset(self):
        return Album.objects.filter(owner=self.request.user).order_by('-created_at')

class AlbumDetailView(DetailView):
    model = Album
    template_name = 'gallery/album_detail.html'
    context_object_name = 'album'

class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'gallery/album_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Album created successfully!")
        return super().form_valid(form)

class AlbumUpdateView(LoginRequiredMixin, IsOwnerOrAdminMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'gallery/album_form.html'
    
    def get_success_url(self):
        messages.success(self.request, "Album updated successfully!")
        return reverse_lazy('album_detail', kwargs={'pk': self.object.pk})

class AlbumDeleteView(LoginRequiredMixin, IsOwnerOrAdminMixin, DeleteView):
    model = Album
    template_name = 'gallery/album_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, "Album deleted successfully!")
        return super().form_valid(form)

class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'gallery/photo_form.html'

    def get_form_kwargs(self):
        kwargs = super(PhotoCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Photo uploaded successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('album_detail', kwargs={'pk': self.object.album.pk})

class PhotoUpdateView(LoginRequiredMixin, IsOwnerOrAdminMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'gallery/photo_form.html'

    def get_form_kwargs(self):
        kwargs = super(PhotoUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        messages.success(self.request, "Photo updated successfully!")
        return reverse_lazy('album_detail', kwargs={'pk': self.object.album.pk})

class PhotoDeleteView(LoginRequiredMixin, IsOwnerOrAdminMixin, DeleteView):
    model = Photo
    template_name = 'gallery/photo_confirm_delete.html'

    def form_valid(self, form):
        if self.object.image:
            try:
                cloudinary.uploader.destroy(self.object.image.public_id)
            except Exception as e:
                print(f"Cloudinary deletion failed: {e}")
        messages.success(self.request, "Photo deleted successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('album_detail', kwargs={'pk': self.object.album.pk})