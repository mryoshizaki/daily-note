from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from .decorators import unauthenticated_user


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        return redirect('login')
    context = {"user": user,}
    return render(request, "index.html", context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, "Username or Password is incorrect.")
            return redirect('login')

    context = {}
    return render(request, "login.html", context)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            User.objects.create(
                user=user,
                name=form.cleaned_data.get('username'),
            )

            subject = 'Daily Note Account Creation Success.'
            message = f'Hi {user.username}, you have successfully registered to Daily Note. We hope you enjoy our services!'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(request, 'Account creation success.')

            return redirect('login')

    context = {'form': form}
    return render(request, "register.html", context)