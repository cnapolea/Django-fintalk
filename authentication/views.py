from django.views.generic import FormView
from django.http import JsonResponse

from .forms import SignUpForm

from django.contrib.auth.models import User

class SignUpFormView(FormView):
    
    form_class = SignUpForm
    template_name = 'sign_up.html'
    success_url = 'login'

def checkEmailAvailability(request):

    context = {}
    email_input = request.GET.get('email')
    email_check = User.objects.filter(email=email_input).values_list('email', flat=True)

    if email_check:
        context["email_available"] = False
    else:
        context["email_available"] = True

    return JsonResponse(context)

def checkUsernameAvailability(request):
    
    context = {}
    username_input = request.GET.get('username')
    print(username_input)
    username_check = User.objects.filter(username=username_input).values_list('username', flat=True)
    print(username_check)
        
    if username_check:
        context["username_available"] =  False
    else:
        context["username_available"] =  True
    
    return JsonResponse(context)

        
   
    
    