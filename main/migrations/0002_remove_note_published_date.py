# Generated by Django 3.2.6 on 2021-12-06 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='published_date',
        ),
    ]
