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
    return render(request, "main/index.html")

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
    return render(request, "main/login.html", context)

@unauthenticated_user
def registerPage(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()

            subject = 'Daily Note Account Creation Success.'
            message = f'Hi {form.cleaned_data.get("username")}, you have successfully registered to Daily Note. We hope you enjoy our services!'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [form.cleaned_data.get("email")]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(request, 'Account creation success.')

            return redirect('login')

    context = {'form': form}
    return render(request, "main/register.html", context)

def logoutPage(request):
    logout(request)
    return render(request, "main/index.html")

def Notes_View(request):
    user = request.user
    notes = Note.objects.get(author = user)
    form = NoteForm()
    if(request.method == POST):
        form = NoteForm({'author':request.user,'title':request.POST.get('title'),'text':request.POST.get('text')})
        if(form.is_valid()):
            form.save
            notes = Note.objects.get(author=user)
            form = NoteForm()
            data = {'notes':notes,'form':form}
            return render(request, 'main/notes/notesview.html')
        else:
            print(form.errors)
    data = {'notes':notes,'form':form}
    return render(request, 'main/notes/NotesView.html',data)