from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from albums.models import Album
from .models import Photo
from .forms import PhotoUploadForm, PhotoEditForm
from dashboard.helpers import log_activity


class PhotoUploadView(LoginRequiredMixin, generic.FormView):
    template_name = 'photos/photo_upload.html'
    form_class = PhotoUploadForm

    def dispatch(self, request, *args, **kwargs):
        self.album = get_object_or_404(Album, slug=kwargs['album_slug'])
        # Only album owner or staff can upload
        if request.user != self.album.owner and not request.user.is_staff:
            messages.error(request, "You don't have permission to upload to this album.")
            return redirect('albums:album_detail', slug=self.album.slug)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        files = self.request.FILES.getlist('images')
        caption = form.cleaned_data.get('caption', '')
        sport_tag = form.cleaned_data.get('sport_tag', '')

        if not files:
            messages.warning(self.request, "No files selected.")
            return self.form_invalid(form)

        count = 0
        for f in files:
            Photo.objects.create(
                album=self.album,
                image=f,
                caption=caption,
                sport_tag=sport_tag,
                uploaded_by=self.request.user,
            )
            count += 1

        log_activity(self.request.user, f'uploaded {count} photo(s)', self.album.title)
        messages.success(self.request, f"{count} photo(s) uploaded to '{self.album.title}'!")
        return redirect('albums:album_detail', slug=self.album.slug)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['album'] = self.album
        return ctx


class PhotoDetailView(generic.DetailView):
    model = Photo
    template_name = 'photos/photo_detail.html'
    context_object_name = 'photo'


class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Photo
    form_class = PhotoEditForm
    template_name = 'photos/photo_edit.html'

    def test_func(self):
        photo = self.get_object()
        return self.request.user == photo.uploaded_by or self.request.user.is_staff

    def get_success_url(self):
        return reverse('albums:album_detail', kwargs={'slug': self.object.album.slug})

    def form_valid(self, form):
        messages.success(self.request, "Photo updated.")
        return super().form_valid(form)


class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Photo
    template_name = 'photos/photo_confirm_delete.html'

    def test_func(self):
        photo = self.get_object()
        return self.request.user == photo.uploaded_by or self.request.user.is_staff

    def get_success_url(self):
        return reverse('albums:album_detail', kwargs={'slug': self.object.album.slug})

    def form_valid(self, form):
        album_title = self.object.album.title
        log_activity(self.request.user, 'deleted photo from', album_title)
        response = super().form_valid(form)
        messages.success(self.request, "Photo deleted.")
        return response
