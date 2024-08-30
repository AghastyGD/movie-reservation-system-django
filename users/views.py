from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.views.generic import FormView
from .forms import CustomUserCreationForm

class SignUp(FormView):
    template_name = 'users/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        user_name = form.cleaned_data.get('username')
        messages.success(self.request, f'Account for the user: {user_name} created successfully. Please log in to continue')
        return super().form_valid(form)
    
class CustomLoginView(LoginView):
    template_name = 'users/login.html' 
    
