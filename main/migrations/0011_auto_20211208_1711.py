# Generated by Django 3.2.9 on 2021-12-08 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_event_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='calendar_id',
        ),
        migrations.DeleteModel(
            name='Calendar',
        ),
    ]