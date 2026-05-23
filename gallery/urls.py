from django.urls import path
from .views import (
    AlbumListView, DashboardView, AlbumDetailView, 
    AlbumCreateView, AlbumUpdateView, AlbumDeleteView,
    PhotoCreateView, PhotoUpdateView, PhotoDeleteView
)

urlpatterns = [
    path('', AlbumListView.as_view(), name='gallery_home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('album/new/', AlbumCreateView.as_view(), name='album_create'),
    path('album/<int:pk>/', AlbumDetailView.as_view(), name='album_detail'),
    path('album/<int:pk>/edit/', AlbumUpdateView.as_view(), name='album_edit'),
    path('album/<int:pk>/delete/', AlbumDeleteView.as_view(), name='album_delete'),
    
    path('photo/new/', PhotoCreateView.as_view(), name='photo_create'),
    path('photo/<int:pk>/edit/', PhotoUpdateView.as_view(), name='photo_edit'),
    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo_delete'),
]
