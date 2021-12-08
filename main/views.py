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
from .serializers import *


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
            loginuser = user
            color = Color.objects.get(user = loginuser)
            data = {'color':color}
            return render(request,"main/index.html",data)
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

            
            user = User.objects.get(username = form.cleaned_data.get('username'))
            colorform = Colorform({'user':user,'value_navbar':"#a75e2f",'value_background':"#e8d9ce"})
            if(colorform.is_valid()):
                colorform.save()
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
    color = Color.objects.get(user = user)
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
    data = {'notes':notes, 'form':form,'color':color}
    return render(request, 'main/notes/NotesView.html',data)
    

def update_note(request,pk):
    user = request.user
    note = Note.objects.get(id=pk)
    color = Color.objects.get(user = user)
    user = note.author
    form = UpdateNoteForm(instance = note)
    if(request.method=="POST"):   
        form = NoteForm({'author':user,'title':request.POST.get('title'),
            'text':request.POST.get('text')}, instance = note)
    
    if form.is_valid():
        form.save()
        notes = Note.objects.filter(author = user)
        data = {"notes":notes,'form':form,'color':color}
        return render(request, "main/notes/notesView.html",data)
    else:
        print(form.errors)
    data = {"note":note,'form':form,'color':color}
    return render(request, "main/notes/update_note.html",data)

def delete_note(request,pk):
    user = request.user
    form = NoteForm()
    try:
        notes = Note.objects.filter(author = user)
        if request.method == 'POST':
            note = Note.objects.get(id=pk)
            note.delete()
    except ObjectDoesNotExist:
        notes = []
    color = Color.objects.get(user = user)
    data = {'notes':notes,'form':form,'color':color}
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


#Calendar

def calendar_view(request):
    color = Color.objects.get(user = request.user)
    if request.POST:
        if request.POST['action'] == 'create':
            form = CalendarForm(request.POST)
            if form.is_valid():
                form.set_owner(request.user)
                form.save()

        if request.POST['action'] == 'edit':
            form = CalendarEditForm(request.POST)
            if form.is_valid():
                form.save(commit=True)

        if request.POST['action'] == 'delete':
            calendar = Calendar.objects.get(calendar_id=request.POST["calendar_id"])
            if calendar.owner == request.user:
                calendar.delete()

    queryset = Calendar.objects.filter(owner=request.user.pk)
    calendars = CalendarSerializer(queryset, many=True).data

    createform = CalendarForm()
    editform = CalendarEditForm(initial={"user_id": request.user.pk, "owner": request.user})

    my_calendars = queryset

    data = {'calendars':calendars, 'createform':createform, 'editform':editform,'my_calendars':my_calendars,'color':color}
    return render(request, 'main/calendar/calendar.html',data)

def Pastel_Themed(request):
    user = request.user
    color = Color.objects.get(user = user)
    colorform = Colorform({'user':user,'value_navbar':"#eeeeee",'value_background':"#d1cfe2"},instance=color)
    if(colorform.is_valid()):
        colorform.save()
        print("it saved")
    else:
        print(colorform.errors)
    color = Color.objects.get(user = user)
    data = {'color':color}
    return render(request, "main/index.html",data)

def Neutral_Themed(request):
    user = request.user
    color = Color.objects.get(user = user)
    colorform = Colorform({'user':user,'value_navbar':"#a75e2f",'value_background':"#e8d9ce"},instance=color)
    if(colorform.is_valid()):
        colorform.save()
        print("it saved")
    else:
        print(colorform.errors)
    color = Color.objects.get(user = user)
    data = {'color':color}
    return render(request, "main/index.html",data)

def Bright_Themed(request):
    user = request.user
    color = Color.objects.get(user = user)
    colorform = Colorform({'user':user,'value_navbar':"#00c69e",'value_background':"#e2c1fe"},instance=color)
    if(colorform.is_valid()):
        colorform.save()
        print("it saved")
    else:
        print(colorform.errors)
    color = Color.objects.get(user = user)
    data = {'color':color}
    return render(request, "main/index.html",data)
