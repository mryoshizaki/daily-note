from django.db import models
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.
class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    text = HTMLField()

    def __str__(self):
        return self.title

class Calendar(models.Model):
    calendar_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    visible_for = models.ManyToManyField(User, related_name="visible_for")
    editable_by = models.ManyToManyField(User, related_name="editable_by")

    def __str__(self):
        return self.name

class Event(models.Model):
    TYPE_CHOICES = [
        ("TASK", 'Task'),
        ("EVENT", 'Event'),
    ]
    event_id = models.AutoField(primary_key=True)
    calendar_id = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    about = models.CharField(max_length=255)
    start_date = models.DateTimeField(null=True,blank=True)
    end_date = models.DateTimeField(null=True,blank=True)
    event_type = models.CharField(max_length=100, choices=TYPE_CHOICES, default="TASK")

    def __str__(self):
        return self.name
