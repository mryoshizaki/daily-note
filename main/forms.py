from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import *
from django.forms import *
from .models import *

class UserForm(UserCreationForm):
    attrs = {'class': 'form-control', 'id': 'floatingInput',
             'placeholder': 'Enter Password', 'required': True}
    password1 = CharField(widget=PasswordInput(attrs=attrs))
    password2 = CharField(widget=PasswordInput(attrs=attrs))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First name', 'aria-label': 'First name', 'required': True}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name', 'aria-label': 'Last name', 'required': True}),
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'aria-label': 'Username', 'required': True}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'aria-label': 'Email', 'required': True}),
        }

class NoteForm(ModelForm):
    class Meta: 
        model = Note
        fields = "__all__"
        widgets = {
            'created_date': DateInput(attrs={'class': 'form-control'}),
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title', 'aria-label': 'Title', 'required': False}),
            'author': HiddenInput(attrs={'type':'hidden'})
        }

class UpdateNoteForm(ModelForm):
    class Meta: 
        model = Note
        fields = "__all__"
        widgets = {
            'created_date': DateInput(attrs={'class': 'form-control'}),
            'text': Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Notes Here', 'aria-label': 'Enter Notes Here', 'required': True}),
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title', 'aria-label': 'Title', 'required': False}),
            'author': HiddenInput(attrs={'type':'hidden'})
        }

class CalendarForm(ModelForm):
    visible_for = CharField(required=False)
    editable_by = CharField(required=False)

    class Meta:
        model = Calendar
        exclude = ['owner', 'editable_by', 'visible_for']
        

    def set_owner(self, user):
        calendar = self.instance
        calendar.owner_id = user.pk
        self.instance = calendar

    def save(self, commit=True):
        calendar = self.instance

        calendar.save()

        for email in self.cleaned_data["visible_for"].split(";"):
            if User.objects.filter(email=email).exists():
                user = User.objects.filter(email=email).get()
                calendar.visible_for.add(user.pk)
        for email in self.cleaned_data["editable_by"].split(";"):
            if User.objects.filter(email=email).exists():
                user = User.objects.filter(email=email).get()
                calendar.editable_by.add(user.pk)

        if commit:
            calendar.save()

        return calendar


def get_calendars(user_id):
    calendars = Calendar.objects.filter(owner=user_id)
    choices = []

    for calendar in calendars:
        choices.append((calendar.pk, calendar.name))

    return choices


class CalendarEditForm(CalendarForm):
    visible_for = CharField(required=False)
    editable_by = CharField(required=False)
    calendar_id = CharField(required=True)

    class Meta:
        model = Calendar
        exclude = ["visible_for", "editable_by",]

    def __init__(self, *args, **kwargs):
        super(CalendarEditForm, self).__init__(*args, **kwargs)
        if self.initial:
            self.fields["calendars"] = ChoiceField(choices=get_calendars(self.initial["user_id"]), required=True)

    def save(self, commit=True):
        calendar = Calendar.objects.get(calendar_id=self.cleaned_data["calendar_id"])
        calendar.name = self.cleaned_data["name"]
        calendar.editable_by.clear()
        calendar.visible_for.clear()

        for email in self.cleaned_data["visible_for"].split(";"):
            if User.objects.filter(email=email).exists():
                user = User.objects.filter(email=email).get()
                calendar.visible_for.add(user.pk)

        for email in self.cleaned_data["editable_by"].split(";"):
            if User.objects.filter(email=email).exists():
                user = User.objects.filter(email=email).get()
                calendar.editable_by.add(user.pk)

        if commit:
            calendar.save()

        return calendar

class EventForm(ModelForm):
    end_date = DateTimeField(input_formats=["%m.%d.%Y %H:%M"], required=True)

    def set_calendar(self, calendar_id):
        event = self.instance
        event.calendar_id = calendar_id
        self.instance = event

    class Meta:
        model = Event
        exclude = ['start_date', 'calendar_id', 'event_id','calendar']
        widgets = {
            'end_date': DateTimeInput(attrs={'class': 'form-control'}),
            'about': Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'aria-label': 'Enter Notes Here', 'required': True}),
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title', 'aria-label': 'Title', 'required': False}),
            'event_type': Select(attrs={'class': 'form-control'})
        }
    