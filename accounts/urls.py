from django.urls import path
from .views import user_login, signUp, home, user_logout


urlpatterns = [
    path('login', user_login, name='login'),
    path('signup', signUp, name='signup'),
    path('home', home, name='home'),
    path('logout', user_logout, name='logout')
]