# Generated by Django 5.0.3 on 2024-04-16 02:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('textbook', '0009_alter_syllabusindicator_indicator_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='syllabusindicator',
            name='syllabus_outcomes',
        ),
    ]
