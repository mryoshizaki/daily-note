# Generated by Django 3.2.9 on 2021-12-07 20:57

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_calendar_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='text',
            field=tinymce.models.HTMLField(),
        ),
    ]
