# Generated by Django 5.0.3 on 2024-04-04 23:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('textbook', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='syllabustopic',
            options={'verbose_name_plural': 'Syllabus Topics'},
        ),
        migrations.AlterField(
            model_name='syllabustopic',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='textbook.subject'),
        ),
    ]
