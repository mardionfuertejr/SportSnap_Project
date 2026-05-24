from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import SignUpView
from .forms import CustomAuthenticationForm

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', LoginView.as_view(authentication_form=CustomAuthenticationForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include('gallery.urls')),
]
