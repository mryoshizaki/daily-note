from django.db import models
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200, null=True)
    text = models.TextField()
    created_date = models.DateTimeField(default = timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class User(models.Model):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    first_name = models.CharField(verbose_name="first name", max_length=20, null=True, blank=True)
    last_name = models.CharField(verbose_name="last name", max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
