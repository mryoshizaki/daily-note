# Generated by Django 3.2.9 on 2021-12-08 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_color_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='color',
            name='color',
        ),
        migrations.AlterField(
            model_name='color',
            name='value_background',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='color',
            name='value_navbar',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
