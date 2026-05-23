from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('albums/', include('albums.urls', namespace='albums')),
    path('photos/', include('photos.urls', namespace='photos')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
]
