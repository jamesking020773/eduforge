from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField
from users.models import UserProfile
from django.utils import timezone

class School(models.Model):
    STATE_CHOICES = [
        ('NSW', 'New South Wales'),
        ('QLD', 'Queensland'),
        ('WA', 'Western Australia'),
        ('TAS', 'Tasmania'),
        ('VIC', 'Victoria'),
        ('NT', 'Northern Territory'),
        ('ACT', 'Australian Capital Territory'),
        ('SA', 'South Australia'),
    ]
    
    admin_first_name = models.CharField(max_length=50, default='')
    admin_surname = models.CharField(max_length=50, default='')
    admin_phone = models.CharField(max_length=50, default='')
    admin_email = models.EmailField(unique=True, default='')
    school_name = models.CharField(max_length=100, default='')
    school_street = models.CharField(max_length=100, default='')
    school_suburb = models.CharField(max_length=100, default='')
    school_postcode = models.PositiveIntegerField(null=True)
    school_state = models.CharField(max_length=3, choices=STATE_CHOICES, default='NSW')
    def __str__(self):
        return self.school_name

class Subject(models.Model):
    LA_CHOICES = [
        ('ENG', 'English'),
        ('MATH', 'Mathematics'),
        ('SCI', 'Science'),
        ('TAS', 'Technological & Applied Studies'),
        ('HSIE', 'Human Society & its Environment'),
        ('CA', 'Creative Arta'),
        ('PDH', 'Personal Development, Health & Physical Eduction'),
        ('LANG', 'Languages'),
        ('VET', 'Vocational Eduaction & Training'),
    ]
    STAGE_CHOICES = [
        ('K', 'Early Stage 1 - Kindergarten'),
        ('1', 'Stage 1 - Years 1 & 2'),
        ('2', 'Stage 2 - Years 3 & 4'),
        ('3', 'Stage 3 - Years 5 & 6'),
        ('4', 'Stage 4 - Years 7 & 8'),
        ('5', 'Stage 5 - Years 9 & 10'),
        ('6', 'Stage 6 - Years 11 & 12'),
    ]
    YEAR_CHOICES = [
        ('K', 'Kindergarten'),
        ('1', 'Year 1'),
        ('2', 'Year 2'),
        ('3', 'Year 3'),
        ('4', 'Year 4'),
        ('5', 'Year 5'),
        ('6', 'Year 6'),
        ('7', 'Year 7'),
        ('8', 'Year 8'),
        ('9', 'Year 9'),
        ('10', 'Year 10'),
        ('11', 'Year 11'),
        ('12', 'Year 12'),
    ]
    subject_name = models.CharField(max_length=100, default='')
    learning_area = models.CharField(max_length=4, choices=LA_CHOICES, default='TAS')
    stage = models.CharField(max_length=1, choices=STAGE_CHOICES, default='6')
    year = models.CharField(max_length=2, choices=YEAR_CHOICES, default='12')
    def __str__(self):
        return self.subject_name

class Textbook(models.Model):
    textbook_number = models.IntegerField(blank=True)
    textbook_title = models.CharField(max_length=200, default='')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='textbook')
    def __str__(self):
        return self.textbook_title

class TextbookTopic(models.Model):
    topic_number = models.IntegerField(blank=True)
    topic_global = models.BooleanField(default=True)
    topic_name = models.CharField(max_length=200, default='')
    textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE, related_name='topics')
    topic_creator = models.ForeignKey('users.UserProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_topics')
    def __str__(self):
        return self.topic_name

class TextbookSection(models.Model):
    section_number = models.IntegerField(blank=True)
    section_global = models.BooleanField(default=True)
    section_title = models.CharField(max_length=200)
    topic = models.ForeignKey(TextbookTopic, on_delete=models.CASCADE, related_name='sections')
    section_creator = models.ForeignKey('users.UserProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_sections')
    def __str__(self):
        return self.section_title

class TextbookPage(models.Model):
    page_number = models.IntegerField(blank=True)
    page_global = models.BooleanField(default=True)
    page_title = models.CharField(max_length=200)
    sections = models.ManyToManyField(TextbookSection, related_name='pages')
    page_creator = models.ForeignKey('users.UserProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_pages')
    def __str__(self):
        return self.page_title

class TextbookSlide(models.Model):
    slide_number = models.IntegerField(blank=True)
    slide_global = models.BooleanField(default=True)
    slide_review= models.BooleanField(default=False)
    slide_title = models.CharField(max_length=200, default='')
    slide_content = models.TextField()
    pages = models.ManyToManyField(TextbookPage, related_name='slides')
    slide_creator = models.ForeignKey('users.UserProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_slides')
    def __str__(self):
        return self.slide_title

class SyllabusOutcome(models.Model):
    outcome_number = models.CharField(max_length=50, default='')
    outcome_description = models.CharField(max_length=200, default='')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='outcomes')
    def __str__(self):
        return f"Outcome {self.outcome_number} - {self.outcome_description}"
    class Meta:
        verbose_name_plural = "Syllabus Outcomes"

class SyllabusTopic(models.Model):
    syllabus_topic_number = models.IntegerField(blank=True)
    syllabus_topic_name = models.CharField(max_length=200, default='')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject')
    outcomes = models.ManyToManyField(SyllabusOutcome, related_name='topics')
    def __str__(self):
        return self.syllabus_topic_name
    class Meta:
        verbose_name_plural = "Syllabus Topics" 

class SyllabusContent(models.Model):
    content_number = models.IntegerField(blank=True)
    content_title = models.CharField(max_length=200, default='')
    syllabus_topic = models.ForeignKey(SyllabusTopic, on_delete=models.CASCADE, related_name='content')
    def __str__(self):
        return self.content_title
    class Meta:
        verbose_name_plural = "Syllabus Content"

class SyllabusIndicator(models.Model):
    indicator_number = models.IntegerField(blank=True)
    indicator_description = models.CharField(max_length=200, default='')
    indicator_skill = models.BooleanField(default=False)
    indicator_knowledge = models.BooleanField(default=True)
    syllabus_content = models.ForeignKey(SyllabusContent, on_delete=models.CASCADE, related_name='indicators')
    def __str__(self):
        return f"{self.indicator_number}. {self.syllabus_content}: {self.indicator_description}"
    class Meta:
        verbose_name_plural = "Syllabus Indicators"
    
class Sequence(models.Model):
    sequence_year = models.IntegerField(blank=True)
    sequence_global = models.BooleanField(default=True)
    sequence_name = models.CharField(max_length=200, default='')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='sequences')
    sequence_creator = models.ForeignKey('users.UserProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_sequence')
    def __str__(self):
        return f" {self.sequence_year} {self.sequence_name} {self.subject}"

class Term(models.Model):
    term_year = models.IntegerField(blank=False)
    term_number = models.IntegerField(blank=False)
    term_start_date = models.DateField(default=timezone.now)
    sequences = models.ManyToManyField(Sequence, related_name='terms')
    def __str__(self):
        return f"Term {self.term_number} of Year {self.term_year}"

class Week(models.Model):
    week_number = models.IntegerField()
    week_start_date = models.DateField(default=timezone.now)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='weeks')
    def __str__(self):
        return f"Week {self.week_number} of Term {self.term.term_number}"

class Lesson(models.Model):
    lesson_number = models.IntegerField(blank=True)
    lesson_global = models.BooleanField(default=True)
    lesson_title = models.CharField(max_length=200)
    learning_intention = models.TextField(default='')
    success_criteria = models.TextField(default='')
    indigenous_perspective = models.TextField(default='')
    differentiation_strategy = models.TextField(default='')
    multi_modal_strategy = models.TextField(default='')
    script = models.TextField(default='')
    introduction_text = models.TextField(default='')
    direct_instruction_text = models.TextField(default='')
    guided_practice_text = models.TextField(default='')
    homwork_text = models.TextField(default='')
    introduction_image = models.CharField(max_length=200, default='')
    direct_instruction_image = models.CharField(max_length=200, default='')
    guided_practice_image = models.CharField(max_length=200, default='')
    homwork_image = models.CharField(max_length=200, default='')
    syllabus_content = models.ManyToManyField(SyllabusContent)
    syllabus_outcomes = models.ManyToManyField(SyllabusOutcome)
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='lessons')
    pages = models.ManyToManyField(TextbookPage)
    lesson_creator = models.ForeignKey('users.UserProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_lesson')
    def __str__(self):
        return self.lesson_title
    
class StudyNote(models.Model):
    note_title = models.CharField(max_length=200, help_text="Enter a title for the study note.")
    note_text = models.TextField(help_text="Enter the study note details.")
    creation_date = models.DateTimeField(auto_now_add=True, help_text="The date and time the note was created.")
    last_updated = models.DateTimeField(auto_now=True, help_text="The date and time the note was last updated.")
    slide = models.ForeignKey(TextbookSlide, on_delete=models.CASCADE, related_name='studynotes', help_text="Select the slide this study note is linked to.")
    note_creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='studynotes', limit_choices_to={'user_type': 'student'}, help_text="The student user who created this study note.")
    def __str__(self):
        return f"{self.note_title} - {self.note_creator.user.username}"
    class Meta:
        verbose_name_plural = "Study Notes"

class Message(models.Model):
    message_timestamp = models.DateTimeField(default=timezone.now, help_text="The date and time the message was created.")
    message_text = models.TextField(help_text="The content of the message.")
    meassge_response = models.TextField(blank=True, null=True, help_text="The optional response to the message.")
    meassage_receipt = models.BooleanField(default=False, help_text="Indicates if the message has been read.")
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='messages', help_text="The subject this message is linked to.")
    message_creator = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='created_messages', help_text="The user who created this message.")
    def __str__(self):
        return f"Message from {self.message_creator.user.username} on {self.message_timestamp.strftime('%Y-%m-%d %H:%M')}"
    def is_accessible_by(self, userprofile):
        if self.creator == userprofile:
            return True
        if self.creator.user_type == 'student' and userprofile.user_type == 'teacher' and self.subject in userprofile.subjects.all():
            return True
        if self.creator.user_type == 'teacher' and userprofile.user_type == 'student' and self.subject in userprofile.subjects.all():
            return True
        return False

class ThinkingLevel(models.Model):
    level_number = models.IntegerField(blank=True)
    level_title = models.CharField(max_length=50, default='')
    level_action = models.CharField(max_length=50, default='')
    level_keyword = models.CharField(max_length=50, default='')
    level_description = models.TextField(default='')
    def __str__(self):
        return f"{self.level_number}. {self.level_description} - {self.level_action}- {self.level_keyword}"
    class Meta:
        verbose_name_plural = "Thinking Levels"

class ExamQuestion(models.Model):
    eq_question_number = models.IntegerField(blank=False)
    eq_question_title = models.CharField(max_length=200, default='')
    eq_question_text = models.TextField(default='')
    eq_question_image = models.CharField(max_length=200, default='')
    eq_answer_text = models.TextField(default='')
    eq_answer_image = models.CharField(max_length=200, default='')
    eq_sample_answer = models.TextField(default='')
    eq_marks_total = models.IntegerField(blank=True)
    eq_marking_criteria = models.TextField(default='')
    eq_marking_rubric = models.TextField(default='')
    eq_writing_scaffold = models.TextField(default='')
    syllabus_outcomes = models.ManyToManyField(SyllabusOutcome, related_name='eq_questions')
    textbook_page = models.ForeignKey(TextbookPage, on_delete=models.CASCADE, related_name='eq_questions')
    thinking_level = models.ForeignKey(ThinkingLevel, on_delete=models.CASCADE, related_name='eq_questions')
    def __str__(self):
        return self.eq_question_title

class RevisionQuestion(models.Model):
    rq_question_number = models.IntegerField(blank=False)
    rq_question_title = models.CharField(max_length=200, default='')
    rq_question_text = models.TextField(default='')
    rq_question_image = models.CharField(max_length=200, default='')
    rq_answer_text = models.TextField(default='')
    rq_answer_image = models.CharField(max_length=200, default='')
    syllabus_outcomes = models.ManyToManyField(SyllabusOutcome, related_name='rq_questions')
    textbook_page = models.ForeignKey(TextbookPage, on_delete=models.CASCADE, related_name='rq_questions')
    thinking_level = models.ForeignKey(ThinkingLevel, on_delete=models.CASCADE, related_name='rq_questions')
    def __str__(self):
        return self.rq_question_title

class CodeQuestion(models.Model):
    cq_question_number = models.IntegerField(blank=False)
    cq_question_title = models.CharField(max_length=200, default='')
    cq_question_text = models.TextField(default='')
    cq_answer_text = models.TextField(default='')
    syllabus_outcomes = models.ManyToManyField(SyllabusOutcome, related_name='cq_questions')
    textbook_page = models.ForeignKey(TextbookPage, on_delete=models.CASCADE, related_name='cq_questions')
    thinking_level = models.ForeignKey(ThinkingLevel, on_delete=models.CASCADE, related_name='cq_questions')
    def __str__(self):
        return self.cq_question_title

class Quiz(models.Model):
    quiz_number = models.IntegerField(blank=False)
    quiz_title = models.CharField(max_length=200, default='')
    quiz_start_date = models.DateField(default=timezone.now)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quiz')
    revision_questions = models.ManyToManyField(RevisionQuestion, related_name='quiz')
    exam_questions = models.ManyToManyField(ExamQuestion, related_name='quiz')
    code_questions = models.ManyToManyField(CodeQuestion, related_name='quiz')
    def __str__(self):
        return f" {self.quiz_title} - {self.quiz_start_date}"

class AssessmentSection(models.Model):
    section_number = models.IntegerField(blank=False)
    section_title = models.CharField(max_length=200, default='')
    rubric_title = models.CharField(max_length=200, default='')
    criteria1_description = models.TextField(default='')
    criteria1_low_mark = models.IntegerField(blank=False)
    criteria1_high_mark = models.IntegerField(blank=False)
    criteria2_description = models.TextField(default='')
    criteria2_low_mark = models.IntegerField(blank=False)
    criteria2_high_mark = models.IntegerField(blank=False)
    criteria3_description = models.TextField(default='')
    criteria3_low_mark = models.IntegerField(blank=False)
    criteria3_high_mark = models.IntegerField(blank=False)
    criteria4_description = models.TextField(default='')
    criteria4_low_mark = models.IntegerField(blank=False)
    criteria4_high_mark = models.IntegerField(blank=False)
    criteria5_description = models.TextField(default='')
    criteria5_low_mark = models.IntegerField(blank=False)
    criteria5_high_mark = models.IntegerField(blank=False)
    def __str__(self):
        return self.section_title

class AssessmentSchedule(models.Model):
    year = models.IntegerField(blank=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assessment_schedule')
    def __str__(self):
        return f" {self.year} - {self.subject}"

class AssessmentTask(models.Model):
    assessment_title = models.CharField(max_length=200, default='')
    task_number = models.IntegerField(blank=False)
    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField(default=timezone.now)
    due_time = models.CharField(max_length=10, default='8am')
    marks = models.IntegerField(blank=False)
    weight = models.IntegerField(blank=False)
    task_description = models.TextField(default='')
    task_requirements = models.TextField(default='')
    submission_requirements = models.TextField(default='')
    resources = models.TextField(default='')
    milestones = models.TextField(default='')
    assessment_sections = models.ManyToManyField(AssessmentSection, related_name='assessment_task')
    assessment_schedule = models.ForeignKey(AssessmentSchedule, on_delete=models.CASCADE, related_name='assessment_task')
    syllabus_outcomes = models.ManyToManyField(SyllabusOutcome, related_name='assessment_task')
    syllabus_topics = models.ManyToManyField(SyllabusTopic, related_name='assessment_task')
    def __str__(self):
        return self.assessment_title

