from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Optional: Assign to a default group if needed
        # user = form.instance
        # group = Group.objects.get(name='Standard User')
        # user.groups.add(group)
        return response
