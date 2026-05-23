from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import RecipePhoto
from .forms import RecipePhotoForm
from django.db.models import Q
from django.contrib import messages
import cloudinary.uploader
# Create your views here.
def gallery_view(request):
    query = request.GET.get('q', '')
    if query:
        photo_list = RecipePhoto.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).order_by('-uploaded_at')
    else:
        photo_list = RecipePhoto.objects.all().order_by('-uploaded_at')
    
    paginator = Paginator(photo_list, 2)
    page_number = request.GET.get('page')
    photos = paginator.get_page(page_number)

    if request.method == 'POST':
        form = RecipePhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery_home')
    else:
        form = RecipePhotoForm()
    
    return render(request, 'gallery/home.html', {
        'form': form,
        'photos': photos,
        'query': query,
    })

def edit_recipe(request, pk):
    photo = get_object_or_404(RecipePhoto, pk=pk)

    if request.method == 'POST':
        # Pass the existing instance to the form so it knows to UPDATE, not create
        form = RecipePhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{photo.title}' updated successfully!")
            return redirect('gallery_home')
    else:
        # Pre-fill the form with the existing data
        form = RecipePhotoForm(instance=photo)
        
    return render(request, 'gallery/edit.html', {'form': form, 'photo': photo})

def delete_recipe(request, pk):
    photo = get_object_or_404(RecipePhoto, pk=pk)
    
    if request.method == 'POST':
        title = photo.title

        if photo.image:
            try:
                # Tell Cloudinary to permanently delete the file from their servers
                cloudinary.uploader.destroy(photo.image.public_id)
            except Exception as e:
                print(f"Cloudinary deletion failed: {e}")

        photo.delete()
        messages.success(request, f"'{title}' was completely deleted.")
        return redirect('gallery_home')
    
    return render(request, 'gallery/delete.html', {'photo': photo})