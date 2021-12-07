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

# class NoteForm(forms.ModelForm):
#     model = Note
#     fields = "__all__"
#     widgets = {
#         'created_date': DateInput(attrs={'class': 'form-control'}),
#         'text': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Notes Here', 'aria-label': 'Enter Notes Here', 'required': True}),
#         'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title', 'aria-label': 'Title', 'required': False}),
#         'author': HiddenInput(attrs={'type':'hidden'})
#     }