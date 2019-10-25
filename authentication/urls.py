from django.urls import path
from django.contrib.auth import views as auth_views

from .views import SignUpFormView, checkEmailAvailability,checkUsernameAvailability

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('sign_up/', SignUpFormView.as_view(), name='sign_up'),
    path('sign_up/ajax/username_verification/', checkUsernameAvailability, name='check_input_availability'),
    path('sign_up/ajax/email_verification/', checkEmailAvailability, name='check_input_availability'),

]