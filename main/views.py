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
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from mysite.settings import EMAIL_HOST_USER


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
    notes = Note.objects.filter(author = user)
    try:
        notes = Note.objects.filter(author = user)
        if request.method == 'POST':
            note = Note.objects.get(id=pk)
            form = NoteForm({'author':request.user,'title':request.POST.get('title'),
                        'text':request.POST.get('text')}, instance = profile)

        # if(form.is_valid()):
        #     form.save()
        #     print("valid")
        #     record = Note.objects.get(id=pk)
        #     profile = Note.objects.get(author=user)
        #     data = {'notes':notes, 'form':form}
        #     return render(request, 'main/notes/updae_note.html',data)

    except ObjectDoesNotExist:
        notes = []

    record = Note.objects.get(id=pk)
    data = {'record':record, 'form':form}
    return render(request, 'main/notes/update_note.html',data)

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

#Reset password -----
def passwordReset(request): 
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
                data = password_reset_form.cleaned_data['email']
                associated_users = User.objects.filter(Q(email=data))
                if associated_users.exists():
                    for user in associated_users:
                        subject = "Password Reset Requested"
                        email_template_name = "main/reset/password_reset_email.txt"
                        c = {
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Reminderific',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        }
                        message = render_to_string(email_template_name, c)
                        try:
                            send_mail(subject, message, EMAIL_HOST_USER , [user.email], fail_silently=False)
                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')
                        return redirect ("done/")

    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="main/reset/password-reset.html", context={"password_reset_form":password_reset_form})
