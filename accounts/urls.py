from django.urls import path
from .views import *
from django.contrib.auth.views import PasswordResetConfirmView


urlpatterns = [
    path('login', user_login, name='login'),
    path('signup', signUp, name='signup'),
    path('logout', user_logout, name='logout'),

    path('forgot-password', forgot_password, name='forgot-password'),
    path('reset-password', reset_password, name='reset-password'),

    path('reset_password_validate/<uidb64>/<token>/', reset_password_validate, name='reset_password_validate')
   

]