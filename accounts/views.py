from django.shortcuts import render
from django.views import generic
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy


class SignUpView(generic.CreateView):
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    form_class = CustomUserCreationForm
    success_message = "Your profile was created successfully"
