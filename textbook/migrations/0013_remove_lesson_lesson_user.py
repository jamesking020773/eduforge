# Generated by Django 5.0.3 on 2024-04-19 00:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('textbook', '0012_lesson_lesson_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='lesson_user',
        ),
    ]
