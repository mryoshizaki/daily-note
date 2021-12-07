from django.db import models
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

