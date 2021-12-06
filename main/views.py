from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from .decorators import unauthenticated_user
from django.core.exceptions import ObjectDoesNotExist


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
    # notes = Note.objects.filter(author = user)
    # notes = []
    try:
        notes = Note.objects.filter(author = user)
    except ObjectDoesNotExist:
        notes = []

    form = NoteForm()
    if request.method == 'POST':
        form = NoteForm({'author':request.user,'title':request.POST.get('title'),
                        'text':request.POST.get('text')})
        if form.is_valid():
            form.save()
            notes = Note.objects.filter(author=user)
            form = NoteForm()
            print("saved form")
            # print(form)
        else:
            print(form.errors)
    data = {'notes':notes, 'form':form}
    return render(request, 'main/notes/NotesView.html',data)
    

def update_note(request,pk):
    user = request.user
    profile = Note.objects.get(author=user)
    form = UpdateNoteForm(instance = profile)
    record = Note.objects.get(id=pk)
    try:
        notes = Note.objects.filter(author = user)
        # if request.method == 'POST':
        #     note = Note.objects.get(id=pk)
        #     form = NoteForm({'author':request.user,'title':request.POST.get('title'),
        #                 'text':request.POST.get('text')}, instance = profile)

        # if(form.is_valid()):
        #     form.save()
        #     print("valid")
        #     profile = Note.objects.get(author=user)
        #     data = {"record":record,'form':form}
        #     return redirect('update-staff')

    except ObjectDoesNotExist:
        notes = []

    data = {'notes':notes}
    return render(request, 'main/notes/NotesView.html',data)

def delete_note(request,pk):
    user = request.user

    try:
        notes = Note.objects.filter(author = user)
        if request.method == 'POST':
            note = Note.objects.get(id=pk)
            note.delete()
    except ObjectDoesNotExist:
        notes = []

    data = {'notes':notes}
    return render(request, 'main/notes/NotesView.html',data)