from django import forms
from .models import Textbook, TextbookTopic, TextbookSection, TextbookPage, TextbookSlide
from .models import Subject, School
from .models import ThinkingLevel
from .models import Sequence, Term, Week, Lesson
from .models import SyllabusTopic, SyllabusOutcome, SyllabusContent, SyllabusIndicator
from django.core.exceptions import ValidationError
from .models import ExamQuestion, RevisionQuestion, CodeQuestion, Quiz
from .models import AssessmentSection, AssessmentSchedule, AssessmentTask
from django.utils import timezone

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__' 
        labels = {
            'admin_first_name': 'Administrator First Name',
            'admin_surname': 'Administrator Surname',
            'admin_phone': 'Administrator Phone',
            'admin_email': 'Administrator Email',
            'school_name': 'School Name',
            'school_street': 'Street',
            'school_suburb': 'Suburb',
            'school_postcode': 'Postcode',
            'school_state': 'State'}

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        labels = {
            'subject_name': 'Subject Name',
            'learning_area': 'Learning Area',
        }

class TextBookPageForm(forms.ModelForm):
    class Meta:
        model = TextbookPage
        fields = '__all__' 
        labels = {
            'page_number': 'Page Number: ',
            'page_title': 'Page Title: ', 
            'page_global': 'Global Defined: ',
            'page_creator': 'Linked Creator: ',
            'sections': 'Linked Sections: ' 
        }
        widgets = {
            'sections': forms.CheckboxSelectMultiple
        }

class TextbookForm(forms.ModelForm):
    class Meta:
        model = Textbook
        fields = '__all__'
        labels = {
            'textbook_title': 'Textbook: ', 
            'subject': 'Subject: '
        }

class TextbookTopicForm(forms.ModelForm):
    class Meta:
        model = TextbookTopic
        fields = '__all__' 
        labels = {
            'topic_number': 'Topic Number: ',
            'topic_name': 'Topic: ',
            'topic_global': 'Global Defined: ',
            'topic_creator': 'Linked Creator: ',
            'textbook': 'Linked Textbook: ',
        }

class TextbookSectionForm(forms.ModelForm):
    class Meta:
        model = TextbookSection
        fields = '__all__'
        labels = {
            'section_number': 'Section Number: ',
            'section_title': 'Section: ',
            'section_global': 'Global Defined: ',
            'topic': 'Linked Topic: ',
            'section_creator': 'Linked Creator: '
        }
        
class TextbookSlideForm(forms.ModelForm):
    class Meta:
        model = TextbookSlide
        fields = '__all__'
        labels = {
            'slide_number': 'Slide Number: ',
            'slide_title': 'Slide Title: ',
            'slide_global': 'Global Defined: ', 
            'slide_review': 'Slide Reviewed: ', 
            'slide_text': 'Slide Text: ',
            'slide_image': 'Slide Image: ',
            'slide_youtube': 'Slide Youtube: ',
            'slide_links': 'Slide Web Links: ',
            'slide_table': 'Slide Table: ',
            'pages': 'Linked Pages: ',
            'slide_creator': 'Creator: '
        }
        widgets = {
            'pages': forms.CheckboxSelectMultiple,
            'slide_table': forms.Textarea(attrs={'cols': 80, 'rows': 20})
        }

class SyllabusTopicForm(forms.ModelForm):
    outcomes = forms.ModelMultipleChoiceField(
        queryset=SyllabusOutcome.objects.none(),  # Default to none, will be set in __init__
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = SyllabusTopic
        fields = '__all__'
        labels = {
            'syllabus_topic': 'Topic: ',
            'subject': 'Linked Subject: ',
            'outcomes': 'Linked Outcomes: ',
        }
    def __init__(self, *args, **kwargs):
        super(SyllabusTopicForm, self).__init__(*args, **kwargs)
        # Adjust the queryset based on the instance or initial subject
        if self.instance and self.instance.pk and self.instance.subject:
            self.fields['outcomes'].queryset = SyllabusOutcome.objects.filter(subject=self.instance.subject)
        elif 'initial' in kwargs and 'subject' in kwargs['initial']:
            self.fields['outcomes'].queryset = SyllabusOutcome.objects.filter(subject=kwargs['initial']['subject'])
        elif self.data and 'subject' in self.data:
            # This handles the case when the form is submitted
            subject_id = self.data.get('subject')
            self.fields['outcomes'].queryset = SyllabusOutcome.objects.filter(subject_id=subject_id)
        else:
            # This is a fallback in case no subject is set
            self.fields['outcomes'].queryset = SyllabusOutcome.objects.none()


class SyllabusOutcomeForm(forms.ModelForm):
    class Meta:
        model = SyllabusOutcome
        fields = '__all__'
        labels = {
            'outcome_number': 'Oucome Number: ', 
            'outcome_description': 'Outcome Description: ', 
            'syllabus_topics': 'Linked Topics: '
        }

class SyllabusContentForm(forms.ModelForm):
    class Meta:
        model = SyllabusContent
        fields = '__all__'
        labels = {
            'content_number': 'Content Number: ', 
            'content_title': 'Content Title: ', 
            'syllabus_topic': 'Linked Topic: '
        }

class SyllabusIndicatorForm(forms.ModelForm):
    class Meta:
        model = SyllabusIndicator
        fields = '__all__'
        labels = {
            'indicator_number': 'Indicator Number: ', 
            'indicator_description': 'Indicator Decription: ', 
            'indicator_skill': 'Skill: ', 
            'indicator_knowledge': 'Knowledge: ', 
            'syllabus_content': 'Linked Content: '
        }

class SequenceForm(forms.ModelForm):
    class Meta:
        model = Sequence
        fields = '__all__'
        labels = {
            'sequence_number': 'Sequence Number: ',     
            'sequence_global': 'Global Defined: ', 
            'sequence_name': 'Sequence Name: ', 
            'subject': 'Linked Subject: ',
            'sequence_creator': 'Creator: '
        }

class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = '__all__'
        labels = {
            'term_number': 'Term Number: ', 
            'term_start_date': 'Term Start Date: ', 
            'sequence': 'Linked Sequence: '
        }
        widgets = {
            'term_start_date': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
        }
    def clean_term_start_date(self):
        term_start_date = self.cleaned_data['term_start_date']
        if term_start_date <= timezone.localdate(): 
            raise ValidationError("The term start date must be in the future.")
        return term_start_date
    

class WeekForm(forms.ModelForm):
    class Meta:
        model = Week
        fields = '__all__'
        labels = {
            'week_number': 'Week Number: ', 
            'week_start_date': 'Week Start Date: ',
            'term': 'Linked Term: '
        }
        widgets = {
            'week_start_date': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
        }
    def clean_week_start_date(self):
        week_start_date = self.cleaned_data['week_start_date']
        if week_start_date <= timezone.localdate(): 
            raise ValidationError("The week start date must be in the future.")
        return week_start_date

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'
        labels = {
            'lesson_number': 'Lesson Number: ', 
            'lesson_global': 'Global Defined: ', 
            'lesson_title': 'Lesson Title: ', 
            'learning_intention': 'Learning Intention: ', 
            'success_riteria': 'Success Criteria: ', 
            'indigenous_perspective': 'Indigenous Perspective: ', 
            'differentiation_strategy': 'Differentiation Strategy: ', 
            'multi_modal_strategy': 'Multi-Modal Strategy: ', 
            'script': 'Teaching Script: ', 
            'introduction_text': 'Introduction Text: ', 
            'introduction_image': 'Introduction Image: ', 
            'direct_instruction_text': 'Direct Instruction Text: ', 
            'direct_instruction_image': 'Direct Instruction Image: ', 
            'guided_practice_text': 'Guided Practice Text: ', 
            'guided_practice_image': 'Guided Practice Image: ', 
            'homwork_text': 'Homework: ', 
            'homwork_image': 'Homework: ', 
            'syllabus_content': 'Linked Topic: ', 
            'syllabus_outcomes': 'Linked Outcomes: ', 
            'week': 'Linked Weeks: ', 
            'pages': 'Linked Pages: '
        }
        widgets = {
            'syllabus_content': forms.CheckboxSelectMultiple,
            'syllabus_outcomes': forms.CheckboxSelectMultiple,
            'pages': forms.CheckboxSelectMultiple,
        }

class ThinkingLevelForm(forms.ModelForm):
    class Meta:
        model = ThinkingLevel
        fields = '__all__'
        labels = {
            'level_number': 'Level Number',
            'level_title': 'Title',
            'level_action': 'Action',
            'level_keyword': 'Key Word',
            'level_description': 'Description',
        }

class ExamQuestionForm(forms.ModelForm):
    class Meta:
        model = ExamQuestion
        fields = '__all__'
        labels = {
            'eq_question_number': 'Question Number',
            'eq_question_title': 'Question Title', 
            'eq_question_text': 'Question Text', 
            'eq_question_image': 'Question Image Path', 
            'eq_answer_text': 'Answer Text', 
            'eq_answer_image': 'Level Number', 
            'eq_sample_answer': 'Level Number', 
            'eq_marks_total': 'Level Number', 
            'eq_marking_criteria': 'Level Number', 
            'eq_marking_rubric': 'Level Number', 
            'eq_writing_scaffold': 'Level Number', 
            'syllabus_outcomes': 'Level Number', 
            'thinking_level': 'Level Number'
        }

class RevisionQuestionForm(forms.ModelForm):
    class Meta:
        model = RevisionQuestion
        fields = '__all__'
        labels = {
            'rq_question_number': 'Question Number', 
            'rq_question_title': 'Question Title', 
            'rq_question_text': 'Question Text', 
            'rq_question_image': 'Question Image Path', 
            'rq_answer_text': 'Answer Text', 
            'rq_answer_image': 'Answer Image Path', 
            'syllabus_outcomes': 'Syllabus Outcomes', 
            'thinking_level': 'Thinking Level'
        }

class CodeQuestionForm(forms.ModelForm):
    class Meta:
        model = CodeQuestion
        fields = '__all__'
        labels = {
            'cq_question_number': 'Question Number', 
            'cq_question_title': 'Question Title', 
            'cq_question_text': 'Question Text', 
            'cq_answer_text': 'Answer Text', 
            'syllabus_outcomes': 'Syllabus Outcomes', 
            'thinking_level': 'Level Number'
        }

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'
        labels = {
            'quiz_number': 'Quiz Number', 
            'quiz_title': 'Quiz Title', 
            'quiz_start_date': 'Quiz Start Date', 
            'subject': 'Linked Subject', 
            'revision_questions': 'Linked Revision Questions', 
            'exam_questions': 'Linked Exam Questions', 
            'code_questions': 'Linked Code Questions'
        }

class AssessmentSectionForm(forms.ModelForm):
    class Meta:
        model = AssessmentSection
        fields = '__all__'
        labels = {
            'section_number': 'Section Number', 
            'section_title': 'Section Title', 
            'rubric_title': 'Rubric Title', 
            'criteria1_description': 'Criteria 1 Description', 
            'criteria1_low_mark': 'Criteria 1 Lowest Mark', 
            'criteria1_high_mark': 'Criteria 1 Highest Mark', 
            'criteria2_description': 'Criteria 2 Description', 
            'criteria2_low_mark': 'Criteria 2 Lowest Mark', 
            'criteria2_high_mark': 'Criteria 2 Highest Mark', 
            'criteria3_description': 'Criteria 3 Description', 
            'criteria3_low_mark': 'Criteria 3 Lowest Mark', 
            'criteria3_high_mark': 'Criteria 3 Highest Mark', 
            'criteria4_description': 'Criteria 4 Description', 
            'criteria4_low_mark': 'Criteria 4 Lowest Mark', 
            'criteria4_high_mark': 'Criteria 4 Highest Mark', 
            'criteria5_description': 'Criteria 5 Description', 
            'criteria5_low_mark': 'Criteria 5 Lowest Mark', 
            'criteria5_high_mark': 'Criteria 5 Highest Mark'
        }

class AssessmentScheduleForm(forms.ModelForm):
    class Meta:
        model = AssessmentSchedule
        fields = '__all__'
        labels = {
            'year': 'Year', 
            'subject': 'Linked Subject'
        }

class AssessmentTaskForm(forms.ModelForm):
    class Meta:
        model = AssessmentTask
        fields = '__all__'
        labels = {
            'assessment_title': 'Assessment Title', 
            'task_number': 'Task Number', 
            'issue_date': 'Issue Date', 
            'due_date': 'Due Date', 
            'due_time': 'Due Time', 
            'marks': 'Raw Marks', 
            'weight': 'Weight (%)', 
            'task_description': 'Task Description', 
            'task_requirements': 'Task Requirements', 
            'submission_requirements': 'Submission Requirements', 
            'resources': 'Resources', 
            'milestones': 'Milestones', 
            'assessment_sections': 'Linked Sections', 
            'assessment_schedule': 'Linked Schedule', 
            'syllabus_outcomes': 'Linked Syllabus Outcomes', 
            'syllabus_topics': 'Linked Syllabus Topics'
        }
