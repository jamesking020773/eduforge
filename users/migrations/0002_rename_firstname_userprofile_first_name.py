# Generated by Django 5.0.3 on 2024-04-04 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='firstname',
            new_name='first_name',
        ),
    ]
