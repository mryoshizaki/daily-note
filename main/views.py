import calendar
from django.http.response import BadHeaderError
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
from datetime import date, datetime, timedelta
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe
from .utils import Calendar
from mysite.settings import EMAIL_HOST_USER

# Create your views here.
def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            loginuser = user
            color = Color.objects.get(user = loginuser)
            data = {'color':color}
            return redirect('dashboard')
        else:
            messages.info(request, "Username or Password is incorrect.")
            return redirect('login')

    context = {}
    return render(request, "main/login.html", context)

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
            return redirect('dashboard')
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
    return redirect('login')

#Notes

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
    form = NoteForm(instance = note)
    if(request.method=="POST"):   
        form = NoteForm({'author':user,'title':request.POST.get('title'),
            'text':request.POST.get('text')}, instance = note)
        if form.is_valid():
            form.save()
            notes = Note.objects.filter(author = user)
            data = {"notes":notes,'form':form,'color':color}
            return render(request, "main/notes/notesView.html",data)
        else:
            print("kldnasldk")
            print(form.errors)
    data = {"note":note,'form':form,'color':color}
    return render(request, "main/notes/update_note.html",data)

def Cancel_Update_Notes(request):

    
    return render(request, 'main/notes/NotesView.html')

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
class CalendarView(generic.ListView):
    model = Event
    template_name = 'main/calendar/calendar.html'

    def get_context_data(self,**kwargs):
        user = self.request.user
        color = Color.objects.get(user = user)
        form = EventForm()
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        # d = get_date(self.request.GET.get('day', None))
        d = get_date(self.request.GET.get('month', None))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(user, withyear=True)
        context['color'] = color
        context['form'] = form
        # context['events'] = events
        # context['request'] = request
        context['calendar'] = mark_safe(html_cal)
        return context
    
    def create_event(self,**kwargs):
        user = self.request.user
        color = Color.objects.get(user = user)
        try:
            events = Event.objects.filter(user = user)
        except ObjectDoesNotExist:
            events = []

        form = EventForm()
        if self.request.method == 'POST':
            form = EventForm({'user':self.request.user,'name':self.request.POST.get('name'),
                            'about':self.request.POST.get('about'),'start_date':self.request.POST.get('start_date'),
                            'end_date':self.request.POST.get('end_date'),'event_type':self.request.POST.get('event_type'),})
            if form.is_valid():
                form.save()
                events = Event.objects.filter(user=user)
                form = EventForm()
                print("saved form")
                data = {'events':events, 'form':form,'color':color}
                return redirect('calendar')
                # print(form)
            else:
                print(form.errors)
        data = {'events':events, 'form':form,'color':color}
        return render(self.request, 'main/calendar/calendar.html',data)
    

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
    

def create_event(request):
    user = request.user
    color = Color.objects.get(user = user)
    try:
        events = Event.objects.filter(user = user)
    except ObjectDoesNotExist:
        events = []

    form = EventForm()
    if request.method == 'POST':
        form = EventForm({'user':request.user,'name':request.POST.get('name'),
                        'about':request.POST.get('about'),'start_date':request.POST.get('start_date'),
                        'end_date':request.POST.get('end_date'),'event_type':request.POST.get('event_type'),})
        if form.is_valid():
            form.save()
            events = Event.objects.filter(user=user)
            form = EventForm()
            print("saved form")
            data = {'events':events, 'form':form,'color':color}
            return redirect('calendar')
            # print(form)
        else:
            print(form.errors)
    data = {'events':events, 'form':form,'color':color}
    return render(request, 'main/calendar/calendar.html',data)

def delete_event(request,pk):
    user = request.user
    color = Color.objects.get(user = user)
    form = EventForm()
    events = Event.objects.filter(user = user).filter(event_type = "Event")
    tasks = Event.objects.filter(user = user).filter(event_type = "Task")

    if request.method == 'POST':
            print('wil del')
            event = Event.objects.get(event_id=pk)
            event.delete()
            return redirect('dashboard')
   
    data = {'events':events,'form':form,'color':color, 'tasks':tasks}
    return render(request, 'main/dashboard.html',data)

def update_event(request,pk):
    user = request.user
    events = Event.objects.get(event_id=pk)
    color = Color.objects.get(user=user)
    form = EventForm(instance = events)
    if(request.method == 'POST'):
        form = EventForm({'user':user,
        'name':request.POST.get('name'),
        'about':request.POST.get('about'),
        'start_date':request.POST.get('start_date'),
        'end_date':request.POST.get('end_date'),
        'event_type':request.POST.get('event_type')},
        instance=events)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            print("kldnasldk")
            print(form.errors)
    data = {"event":events,'form':form,'color':color}
    return render(request, "main/calendar/update_event.html",data)

#Theme

def Pastel_Themed(request):
    user = request.user
    color = Color.objects.get(user = user)

    events = Event.objects.filter(user=user).filter(event_type="Event")
    event_count = events.count()
    tasks = Event.objects.filter(user=user).filter(event_type="Task")
    task_count = tasks.count()
    notExist = ""  

    colorform = Colorform({'user':user,'value_navbar':"#eeeeee",'value_background':"#d1cfe2"},instance=color)
    if(colorform.is_valid()):
        colorform.save()
        print("it saved")
    else:
        print(colorform.errors)
    color = Color.objects.get(user = user)
    data = {'color':color,'notExist':notExist, 'events':events, 'tasks':tasks, 'event_count':event_count, 'task_count':task_count }
    return render(request, "main/dashboard.html",data)

def Neutral_Themed(request):
    user = request.user
    color = Color.objects.get(user = user)

    events = Event.objects.filter(user=user).filter(event_type="Event")
    event_count = events.count()
    tasks = Event.objects.filter(user=user).filter(event_type="Task")
    task_count = tasks.count()
    notExist = ""  

    colorform = Colorform({'user':user,'value_navbar':"#a75e2f",'value_background':"#e8d9ce"},instance=color)
    if(colorform.is_valid()):
        colorform.save()
        print("it saved")
    else:
        print(colorform.errors)
    color = Color.objects.get(user = user)
    data = {'color':color,'notExist':notExist, 'events':events, 'tasks':tasks, 'event_count':event_count, 'task_count':task_count }
    return render(request, "main/dashboard.html",data)

def Bright_Themed(request):
    user = request.user
    color = Color.objects.get(user = user)
    
    events = Event.objects.filter(user=user).filter(event_type="Event")
    event_count = events.count()
    tasks = Event.objects.filter(user=user).filter(event_type="Task")
    task_count = tasks.count()
    notExist = ""    
    
    colorform = Colorform({'user':user,'value_navbar':"#f5e45f",'value_background':"#e2c1f3"},instance=color)
    if(colorform.is_valid()):
        colorform.save()
        print("it saved")
    else:
        print(colorform.errors)
    color = Color.objects.get(user = user)
    data = {'color':color,'notExist':notExist, 'events':events, 'tasks':tasks, 'event_count':event_count, 'task_count':task_count }
    return render(request, "main/dashboard.html",data)

#dashboard

def dashboard(request):
    user = request.user
    color = Color.objects.get(user = user)
    events = Event.objects.filter(user=user).filter(event_type="Event").order_by('start_date')
    event_count = events.count()
    tasks = Event.objects.filter(user=user).filter(event_type="Task").order_by('end_date')
    task_count = tasks.count() 
    form = EventForm() 
    data = {'color':color, 'events':events, 'tasks':tasks, 'event_count':event_count, 'task_count':task_count, 'form':form}
    return render(request, "main/dashboard.html",data)

#help
def about(request):
    user = request.user
    color = Color.objects.get(user = user)
    data = {'color':color}
    return render(request, "main/help/about.html", data)

def help_dashboard(request):
    user = request.user
    color = Color.objects.get(user = user)
    data = {'color':color}
    return render(request, "main/help/helpdashboard.html", data)

def help_calendar(request):
    user = request.user
    color = Color.objects.get(user = user)
    data = {'color':color}
    return render(request, "main/help/helpcalendar.html", data)

def help_notes(request):
    user = request.user
    color = Color.objects.get(user = user)
    data = {'color':color}
    return render(request, "main/help/helpnotes.html", data)

def help_themes(request):
    user = request.user
    color = Color.objects.get(user = user)
    data = {'color':color}
    return render(request, "main/help/helpthemes.html", data)
