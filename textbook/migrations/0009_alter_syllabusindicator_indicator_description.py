# Generated by Django 5.0.3 on 2024-04-16 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('textbook', '0008_remove_textbookslide_slide_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='syllabusindicator',
            name='indicator_description',
            field=models.CharField(default='', max_length=200),
        ),
    ]
