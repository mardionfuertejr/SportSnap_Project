from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery_view, name='gallery_home'),
    path('recipe/<int:pk>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipe/<int:pk>/delete/', views.delete_recipe, name='delete_recipe'),
]

