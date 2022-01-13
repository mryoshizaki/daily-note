# Generated by Django 3.2.9 on 2021-12-08 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_note_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=20, null=True)),
                ('value_navbar', models.CharField(default='#eeeeee', max_length=10, null=True)),
                ('value_background', models.CharField(default='#d1cfe2', max_length=10, null=True)),
            ],
        ),
    ]
