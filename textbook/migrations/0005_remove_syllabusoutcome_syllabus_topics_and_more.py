# Generated by Django 5.0.3 on 2024-04-04 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('textbook', '0004_alter_syllabusoutcome_outcome_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='syllabusoutcome',
            name='syllabus_topics',
        ),
        migrations.AddField(
            model_name='syllabusindicator',
            name='syllabus_outcomes',
            field=models.ManyToManyField(related_name='outcomes', to='textbook.syllabusoutcome'),
        ),
    ]