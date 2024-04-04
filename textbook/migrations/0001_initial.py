# Generated by Django 5.0.3 on 2024-04-03 23:06

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssessmentSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AssessmentSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_number', models.IntegerField()),
                ('section_title', models.CharField(default='', max_length=200)),
                ('rubric_title', models.CharField(default='', max_length=200)),
                ('criteria1_description', models.TextField(default='')),
                ('criteria1_low_mark', models.IntegerField()),
                ('criteria1_high_mark', models.IntegerField()),
                ('criteria2_description', models.TextField(default='')),
                ('criteria2_low_mark', models.IntegerField()),
                ('criteria2_high_mark', models.IntegerField()),
                ('criteria3_description', models.TextField(default='')),
                ('criteria3_low_mark', models.IntegerField()),
                ('criteria3_high_mark', models.IntegerField()),
                ('criteria4_description', models.TextField(default='')),
                ('criteria4_low_mark', models.IntegerField()),
                ('criteria4_high_mark', models.IntegerField()),
                ('criteria5_description', models.TextField(default='')),
                ('criteria5_low_mark', models.IntegerField()),
                ('criteria5_high_mark', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CodeQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cq_question_number', models.IntegerField()),
                ('cq_question_title', models.CharField(default='', max_length=200)),
                ('cq_question_text', models.TextField(default='')),
                ('cq_answer_text', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='ExamQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eq_question_number', models.IntegerField()),
                ('eq_question_title', models.CharField(default='', max_length=200)),
                ('eq_question_text', models.TextField(default='')),
                ('eq_question_image', models.CharField(default='', max_length=200)),
                ('eq_answer_text', models.TextField(default='')),
                ('eq_answer_image', models.CharField(default='', max_length=200)),
                ('eq_sample_answer', models.TextField(default='')),
                ('eq_marks_total', models.IntegerField(blank=True)),
                ('eq_marking_criteria', models.TextField(default='')),
                ('eq_marking_rubric', models.TextField(default='')),
                ('eq_writing_scaffold', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_number', models.IntegerField(blank=True)),
                ('lesson_global', models.BooleanField(default=True)),
                ('lesson_user', models.BooleanField(default=True)),
                ('lesson_title', models.CharField(max_length=200)),
                ('learning_intention', models.TextField(default='')),
                ('success_criteria', models.TextField(default='')),
                ('indigenous_perspective', models.TextField(default='')),
                ('differentiation_strategy', models.TextField(default='')),
                ('multi_modal_strategy', models.TextField(default='')),
                ('script', models.TextField(default='')),
                ('introduction_text', models.TextField(default='')),
                ('direct_instruction_text', models.TextField(default='')),
                ('guided_practice_text', models.TextField(default='')),
                ('homwork_text', models.TextField(default='')),
                ('introduction_image', models.CharField(default='', max_length=200)),
                ('direct_instruction_image', models.CharField(default='', max_length=200)),
                ('guided_practice_image', models.CharField(default='', max_length=200)),
                ('homwork_image', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_timestamp', models.DateTimeField(default=django.utils.timezone.now, help_text='The date and time the message was created.')),
                ('message_text', models.TextField(help_text='The content of the message.')),
                ('meassge_response', models.TextField(blank=True, help_text='The optional response to the message.', null=True)),
                ('meassage_receipt', models.BooleanField(default=False, help_text='Indicates if the message has been read.')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz_number', models.IntegerField()),
                ('quiz_title', models.CharField(default='', max_length=200)),
                ('quiz_start_date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='RevisionQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rq_question_number', models.IntegerField()),
                ('rq_question_title', models.CharField(default='', max_length=200)),
                ('rq_question_text', models.TextField(default='')),
                ('rq_question_image', models.CharField(default='', max_length=200)),
                ('rq_answer_text', models.TextField(default='')),
                ('rq_answer_image', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_first_name', models.CharField(default='', max_length=50)),
                ('admin_surname', models.CharField(default='', max_length=50)),
                ('admin_phone', models.CharField(default='', max_length=50)),
                ('admin_email', models.EmailField(default='', max_length=254, unique=True)),
                ('school_name', models.CharField(default='', max_length=100)),
                ('school_street', models.CharField(default='', max_length=100)),
                ('school_suburb', models.CharField(default='', max_length=100)),
                ('school_postcode', models.PositiveIntegerField(null=True)),
                ('school_state', models.CharField(choices=[('NSW', 'New South Wales'), ('QLD', 'Queensland'), ('WA', 'Western Australia'), ('TAS', 'Tasmania'), ('VIC', 'Victoria'), ('NT', 'Northern Territory'), ('ACT', 'Australian Capital Territory'), ('SA', 'South Australia')], default='NSW', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence_year', models.IntegerField(blank=True)),
                ('sequence_global', models.BooleanField(default=True)),
                ('sequence_name', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='StudyNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note_title', models.CharField(help_text='Enter a title for the study note.', max_length=200)),
                ('note_text', models.TextField(help_text='Enter the study note details.')),
                ('creation_date', models.DateTimeField(auto_now_add=True, help_text='The date and time the note was created.')),
                ('last_updated', models.DateTimeField(auto_now=True, help_text='The date and time the note was last updated.')),
            ],
            options={
                'verbose_name_plural': 'Study Notes',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(default='', max_length=100)),
                ('learning_area', models.CharField(choices=[('ENG', 'English'), ('MATH', 'Mathematics'), ('SCI', 'Science'), ('TAS', 'Technological & Applied Studies'), ('HSIE', 'Human Society & its Environment'), ('CA', 'Creative Arta'), ('PDH', 'Personal Development, Health & Physical Eduction'), ('LANG', 'Languages'), ('VET', 'Vocational Eduaction & Training')], default='TAS', max_length=4)),
                ('stage', models.CharField(choices=[('K', 'Early Stage 1 - Kindergarten'), ('1', 'Stage 1 - Years 1 & 2'), ('2', 'Stage 2 - Years 3 & 4'), ('3', 'Stage 3 - Years 5 & 6'), ('4', 'Stage 4 - Years 7 & 8'), ('5', 'Stage 5 - Years 9 & 10'), ('6', 'Stage 6 - Years 11 & 12')], default='6', max_length=1)),
                ('year', models.CharField(choices=[('K', 'Kindergarten'), ('1', 'Year 1'), ('2', 'Year 2'), ('3', 'Year 3'), ('4', 'Year 4'), ('5', 'Year 5'), ('6', 'Year 6'), ('7', 'Year 7'), ('8', 'Year 8'), ('9', 'Year 9'), ('10', 'Year 10'), ('11', 'Year 11'), ('12', 'Year 12')], default='12', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='SyllabusContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_number', models.IntegerField(blank=True)),
                ('content_title', models.CharField(default='', max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Syllabus Content',
            },
        ),
        migrations.CreateModel(
            name='SyllabusIndicator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indicator_number', models.IntegerField(blank=True)),
                ('indicator_description', models.TextField(default='')),
                ('indicator_skill', models.BooleanField(default=False)),
                ('indicator_knowledge', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Syllabus Indicators',
            },
        ),
        migrations.CreateModel(
            name='SyllabusOutcome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outcome_number', models.CharField(default='', max_length=50)),
                ('outcome_description', models.TextField(default='')),
            ],
            options={
                'verbose_name_plural': 'Syllabus Outcomes',
            },
        ),
        migrations.CreateModel(
            name='SyllabusTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('syllabus_topic', models.CharField(default='', max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Syllabi',
            },
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term_year', models.IntegerField()),
                ('term_number', models.IntegerField()),
                ('term_start_date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Textbook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('textbook_title', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TextbookPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_number', models.IntegerField(blank=True)),
                ('page_global', models.BooleanField(default=True)),
                ('page_title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TextbookSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_number', models.IntegerField(blank=True)),
                ('section_global', models.BooleanField(default=True)),
                ('section_title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TextbookSlide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slide_number', models.IntegerField(blank=True)),
                ('slide_global', models.BooleanField(default=True)),
                ('slide_review', models.BooleanField(default=False)),
                ('slide_title', models.CharField(default='', max_length=200)),
                ('slide_text', models.TextField(default='')),
                ('slide_image', models.CharField(default='', max_length=200)),
                ('slide_youtube', models.CharField(default='', max_length=200)),
                ('slide_links', models.CharField(default='', max_length=500)),
                ('slide_table', models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='TextbookTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_number', models.IntegerField(blank=True)),
                ('topic_global', models.BooleanField(default=True)),
                ('topic_name', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ThinkingLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level_number', models.IntegerField(blank=True)),
                ('level_title', models.CharField(default='', max_length=50)),
                ('level_action', models.CharField(default='', max_length=50)),
                ('level_keyword', models.CharField(default='', max_length=50)),
                ('level_description', models.TextField(default='')),
            ],
            options={
                'verbose_name_plural': 'Thinking Levels',
            },
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_number', models.IntegerField()),
                ('week_start_date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='AssessmentTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assessment_title', models.CharField(default='', max_length=200)),
                ('task_number', models.IntegerField()),
                ('issue_date', models.DateField(default=django.utils.timezone.now)),
                ('due_date', models.DateField(default=django.utils.timezone.now)),
                ('due_time', models.CharField(default='8am', max_length=10)),
                ('marks', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('task_description', models.TextField(default='')),
                ('task_requirements', models.TextField(default='')),
                ('submission_requirements', models.TextField(default='')),
                ('resources', models.TextField(default='')),
                ('milestones', models.TextField(default='')),
                ('assessment_schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessment_task', to='textbook.assessmentschedule')),
                ('assessment_sections', models.ManyToManyField(related_name='assessment_task', to='textbook.assessmentsection')),
            ],
        ),
    ]
