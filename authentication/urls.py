from django.urls import path
from django.contrib.auth import views as auth_views

from .views import SignUpFormView, check_email_availability,check_username_availability

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name = 'signIn'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('sign_up/', SignUpFormView.as_view(), name='sign_up'),
    path('sign_up/ajax/username_verification/', check_username_availability, name='check_input_availability'),
    path('sign_up/ajax/email_verification/', check_email_availability, name='check_input_availability'),

]