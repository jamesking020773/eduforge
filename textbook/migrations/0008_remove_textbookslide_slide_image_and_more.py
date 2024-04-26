# Generated by Django 5.0.3 on 2024-04-11 03:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('textbook', '0007_syllabustopic_outcomes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='textbookslide',
            name='slide_image',
        ),
        migrations.RemoveField(
            model_name='textbookslide',
            name='slide_links',
        ),
        migrations.RemoveField(
            model_name='textbookslide',
            name='slide_table',
        ),
        migrations.RemoveField(
            model_name='textbookslide',
            name='slide_text',
        ),
        migrations.RemoveField(
            model_name='textbookslide',
            name='slide_youtube',
        ),
        migrations.AddField(
            model_name='textbookslide',
            name='slide_content',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='syllabustopic',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='syllabustopic_set', to='textbook.subject'),
        ),
    ]
