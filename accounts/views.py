from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def home(request):
    return render(request, 'main_templates/home.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            # messages.success(request, 'you are logged in...')
            return redirect('home')
        else:
            messages.warning(request, 'invalid crendentials')
            return redirect('login')
    return render(request, 'accounts/login.html')


def signUp(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'email already exists')
            return redirect("signup")
        else:
            if password1 == password2:
                user = User.objects.create_user(username=username, email=email,  password=password1)
                user.save()
                messages.success(request, 'Account created successfully')
                return redirect("login")
            else:
                messages.warning(request, 'passwords does not match')
                return redirect('signup')
        
    return render(request, 'accounts/signup.html')


def user_logout(request):
    logout(request)
    return redirect('login')