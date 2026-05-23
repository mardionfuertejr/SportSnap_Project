from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import RegistrationForm, ProfileForm
from .models import Profile


class RegisterView(generic.CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f"Welcome to SportSnap, {user.username}! Your account is ready.")
        return redirect(self.success_url)


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        remember = self.request.POST.get('remember_me')
        if not remember:
            self.request.session.set_expiry(0)
        messages.success(self.request, f"Welcome back, {form.get_user().username}!")
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "You've been logged out. See you next time!")
        return super().dispatch(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)


class UserListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return User.objects.select_related('profile').order_by('-date_joined')


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('accounts:user_list')

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        # Admins can't delete themselves
        return User.objects.exclude(pk=self.request.user.pk)

    def form_valid(self, form):
        username = self.object.username
        response = super().form_valid(form)
        messages.success(self.request, f"User '{username}' has been removed.")
        return response
