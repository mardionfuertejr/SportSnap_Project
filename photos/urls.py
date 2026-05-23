from django.urls import path
from . import views

app_name = 'photos'

urlpatterns = [
    path('upload/<slug:album_slug>/', views.PhotoUploadView.as_view(), name='photo_upload'),
    path('<int:pk>/', views.PhotoDetailView.as_view(), name='photo_detail'),
    path('<int:pk>/edit/', views.PhotoUpdateView.as_view(), name='photo_edit'),
    path('<int:pk>/delete/', views.PhotoDeleteView.as_view(), name='photo_delete'),
]
