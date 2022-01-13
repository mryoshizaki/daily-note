from typing import Reversible
from django.db import models
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User
from tinymce.models import HTMLField


TYPE_CHOICES = [
        ("TASK", 'Task'),
        ("EVENT", 'Event'),
    ]



# Create your models here.
class Color(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    value_navbar = models.CharField(max_length=10,null=True)
    value_background = models.CharField(max_length=10,null=True)

    def __str__(self):
        return self.user.username

class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    text = HTMLField()

    def __str__(self):
        return self.title

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    event_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    about = models.CharField(max_length=255)
    start_date = models.DateTimeField(null=True,blank=True)
    end_date = models.DateTimeField(null=True,blank=True)
    event_type = models.CharField(max_length=100, choices=TYPE_CHOICES, default="TASK")

    def __str__(self):
        return self.name 

    @property
    def get_html_url(self):
        url = Reversible('event_edit', args=(self.id,))
        return f'<p>{self.name}</p><a href="{url}">edit</a>'
