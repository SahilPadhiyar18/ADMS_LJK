from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from ljwebsite_module.settings import *
from .utils import *
from django.utils.http import urlsafe_base64_decode

# Create your views here.


def user_login(request):
    try:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                # messages.success(request, 'you are logged in...')
                return redirect('home')
            else:
                try:
                    _user = User.objects.get(email=email)
                except Exception as e:
                    _user = None
                if _user:
                     messages.warning(request, 'invalid crendentials')
                else:
                     messages.warning(request, 'don\'t have an account ! please create one')
                return redirect('login')
        return render(request, 'accounts/login.html')
    except Exception as e:
        return render(request, 'accounts/login.html')


def signUp(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'username already exists')
                return redirect("signup")
            elif User.objects.filter(email=email).exists():
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
    except Exception as e:
        return render(request, 'accounts/signup.html')



def user_logout(request):
    logout(request)
    return redirect('login')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successfully')
            return redirect('login')
        else:
            messages.warning(request, 'Password do not match!')
            return redirect('reset-password')
        
    return render(request, 'accounts/reset_password.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = 'Reset Your Password'
            email_template = 'accounts/email_template.html'
            send_verification_email(request, user, mail_subject, email_template)

            context = {
                'msg': 'Password Reset Link hase been sent to your email address!  Please check your email'
            }
            return render(request, 'accounts/email_sent_status.html', context)
        else:
            context = {
                'msg': 'We don\'t have a user having given email address.'
            }
            return render(request, 'accounts/email_sent_status.html', context)

    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        return redirect('reset-password')
    else:
        messages.warning(request, 'This link has been expired!')
        return redirect('login')


