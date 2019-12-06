from django.views.generic import FormView
from django.shortcuts import redirect, get_object_or_404, reverse
from django.contrib.auth.models import User
from django.urls import reverse_lazy


from .forms import SignUpForm
from talks.models import Talk

class SignUpFormView(FormView):
    """This generic class view deals with users' first registration to the website"""
    
    form_class = SignUpForm
    template_name = 'sign_up.html'
    success_url = reverse_lazy('signIn')

    def form_valid(self, form):
        response = super().form_valid(form)
        
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        username = form.cleaned_data['username']
        email = form.cleaned_data['email'].title()
        password = form.cleaned_data['password1']

        new_user = User.objects.create_user(username, email, 
                    password, first_name=first_name, 
                    last_name=last_name)
        return response

