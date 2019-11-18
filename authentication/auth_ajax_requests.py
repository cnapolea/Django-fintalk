from django.contrib.auth.models import User
from django.http import JsonResponse
def check_email_availability(request):

    """This function sends true or false to an ajax request to inform the user if an email is taken or not."""

    context = {}
    email_input = request.GET.get('email')
    email_check = User.objects.filter(
                    email=email_input.title()).values_list(
                                                'email', flat=True)

    if email_check:
        context["email_available"] = False
    else:
        context["email_available"] = True

    return JsonResponse(context)

def check_username_availability(request):
    """This function sends true or false to an ajax request to inform the user if an username is taken or not."""

    context = {}
    username_input = request.GET.get('username')
    username_check = User.objects.filter(
                        username=username_input).values_list(
                                                    'username', flat=True)
    
        
    if username_check:
        context["username_available"] =  False
    else:
        context["username_available"] =  True
    
    return JsonResponse(context)
