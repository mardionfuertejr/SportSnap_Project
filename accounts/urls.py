from django.urls import path
from django.contrib.auth.views import LoginView
from .views import SignUpView
from .forms import CustomAuthenticationForm

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', LoginView.as_view(authentication_form=CustomAuthenticationForm), name='login'),
]
