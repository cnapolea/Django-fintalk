from django.views.generic import FormView
from django.http import JsonResponse
from django.urls import reverse_lazy

from .forms import SignUpForm

from django.contrib.auth.models import User

class SignUpFormView(FormView):
    
    form_class = SignUpForm
    template_name = 'sign_up.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        username = form.cleaned_data['username']
        email = form.cleaned_data['email'].title()
        password = form.cleaned_data['password1']

        new_user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
        return response
        

def check_email_availability(request):

    context = {}
    email_input = request.GET.get('email')
    email_check = User.objects.filter(email=email_input.title()).values_list('email', flat=True)
    print(email_input)
    print(email_check)

    if email_check:
        context["email_available"] = False
    else:
        context["email_available"] = True

    return JsonResponse(context)

def check_username_availability(request):
    
    context = {}
    username_input = request.GET.get('username')
    username_check = User.objects.filter(username=username_input).values_list('username', flat=True)
    
        
    if username_check:
        context["username_available"] =  False
    else:
        context["username_available"] =  True
    
    return JsonResponse(context)
