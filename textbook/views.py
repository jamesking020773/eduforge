from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from users.models import UserProfile
from django.core import serializers
from django.core.serializers import serialize
from django.shortcuts import render
from .models import Textbook, TextbookTopic, TextbookSection, TextbookPage, TextbookSlide
from .models import ExamQuestion, RevisionQuestion, CodeQuestion
from .models import Term, Week, Lesson, School, Subject, Sequence
from .models import SyllabusTopic, SyllabusOutcome, SyllabusContent, SyllabusIndicator
from .forms import ExamQuestionForm, RevisionQuestionForm, CodeQuestionForm
from .forms import TermForm, WeekForm, SchoolForm, SubjectForm
from .forms import SyllabusTopicForm, SyllabusOutcomeForm, SyllabusContentForm, SyllabusIndicatorForm
from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Subquery, Count
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from collections import defaultdict
from django.http import JsonResponse
import json
from django.utils.safestring import mark_safe
from django.db.models import Prefetch
from django.http import HttpResponse
from django.template.loader import render_to_string

@login_required
def index(request):
    schools_list = ''
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            schools_list = user_profile.schools.all() 
        except UserProfile.DoesNotExist:
            schools_list = 'No schools associated'
    else:
        return HttpResponseRedirect(reverse("users:login"))
    questions = ExamQuestion.objects.all()
    questions_json = serializers.serialize('json', questions)
    return render(request, 'textbook/index.html', {
            'schools_list': schools_list,
            'questions_json': questions_json
        })

def get_topics_by_subject(request, subject_id):
    topics = SyllabusTopic.objects.filter(subject_id=subject_id).values('id', 'syllabus_topic_name')
    return JsonResponse(list(topics), safe=False)

def get_sequences_by_subject(request, subject_id):
    sequences = Sequence.objects.filter(subject_id=subject_id).values('id', 'sequence_year').order_by('sequence_year')
    return JsonResponse(list(sequences), safe=False)

def get_terms_by_sequence(request, sequence_id):
    terms = Term.objects.filter(sequences__id=sequence_id).values('id', 'term_number').order_by('term_number')
    return JsonResponse(list(terms), safe=False)

def get_weeks_by_term(request, term_id):
    weeks = Week.objects.filter(term_id=term_id).values('id', 'week_number').order_by('week_number')
    return JsonResponse(list(weeks), safe=False)

def get_lessons_by_week(request, week_id):
    lessons = Lesson.objects.filter(week_id=week_id).values('id', 'lesson_number', 'lesson_title').order_by('lesson_number')
    return JsonResponse(list(lessons), safe=False)

def get_pages_by_lesson(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    pages = lesson.pages.all().values('id', 'page_title', 'page_number').order_by('page_number')
    return JsonResponse(list(pages), safe=False)

def get_slides_by_page(request, page_id):
    slides = TextbookSlide.objects.filter(pages=page_id).values('id', 'slide_title', 'slide_number', 'slide_content').order_by('slide_number')
    return JsonResponse(list(slides), safe=False)

def get_textbooks_by_subject(request, subject_id):
    textbooks = Textbook.objects.filter(subject_id=subject_id).values('id', 'textbook_title')
    return JsonResponse(list(textbooks), safe=False)

def get_topics_by_textbook(request, textbook_id):
    topics = TextbookTopic.objects.filter(textbook_id=textbook_id).values('id', 'topic_number', 'topic_name')
    return JsonResponse(list(topics), safe=False)

def get_sections_by_topic(request, topic_id):
    sections = TextbookSection.objects.filter(topic_id=topic_id).values('id', 'section_number', 'section_title').order_by('section_number')
    return JsonResponse(list(sections), safe=False)

def get_pages_by_section(request, section_id):
    sections = TextbookSection.objects.get(id=section_id)
    pages = sections.pages.all().values('id', 'page_number', 'page_title').order_by('page_number')
    return JsonResponse(list(pages), safe=False)

def syllabus_topic_edit(request, pk=None):
    if pk:
        topic = SyllabusTopic.objects.get(pk=pk)
        form = SyllabusTopicForm(instance=topic)
    else:
        form = SyllabusTopicForm()
    if request.is_ajax():
        html = render_to_string('textbook/syllabus_topic_form.html', {'form': form}, request=request)
        return HttpResponse(html)

class LessonSchedule(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'textbook/lesson_schedule.html'
    context_object_name = 'learning_areas_with_subjects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subjects = Subject.objects.all()
        learning_areas_with_subjects = defaultdict(list)
        
        # Organise subjects by learning area
        for subject in subjects:
            learning_area_display = dict(Subject.LA_CHOICES).get(subject.learning_area, "Unknown Learning Area")
            learning_areas_with_subjects[learning_area_display].append({
                'id': subject.id,
                'name': subject.subject_name
            })
        
        # Convert defaultdict to regular dict for template compatibility
        context['learning_areas_with_subjects'] = dict(learning_areas_with_subjects)
        
        return context
  
class StudyMaterials(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'textbook/study_materials.html'
    context_object_name = 'learning_areas_with_subjects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subjects = Subject.objects.all()
        learning_areas_with_subjects = defaultdict(list)
        
        # Organise subjects by learning area
        for subject in subjects:
            learning_area_display = dict(Subject.LA_CHOICES).get(subject.learning_area, "Unknown Learning Area")
            learning_areas_with_subjects[learning_area_display].append({
                'id': subject.id,
                'name': subject.subject_name
            })
        
        # Convert defaultdict to regular dict for template compatibility
        context['learning_areas_with_subjects'] = dict(learning_areas_with_subjects)
        
        return context

class QuestionCreate(LoginRequiredMixin, CreateView):
    model = ExamQuestion
    form_class = ExamQuestionForm
    template_name = 'textbook/question_form.html'
    success_url = reverse_lazy('textbook:question_list')

class QuestionUpdate(LoginRequiredMixin, UpdateView):
    model = ExamQuestion
    form_class = ExamQuestionForm
    template_name = 'textbook/question_form.html'
    success_url = reverse_lazy('textbook:question_list')

class QuestionDelete(LoginRequiredMixin, DeleteView):
    model = ExamQuestion
    success_url = reverse_lazy('textbook:question_list')

class QuestionList(LoginRequiredMixin, ListView):
    model = ExamQuestion
    context_object_name = 'questions'
    template_name = 'textbook/question_list.html'

class TermCreate(LoginRequiredMixin, CreateView):
    model = Term
    form_class = TermForm
    template_name = 'textbook/term_form.html'
    success_url = reverse_lazy('textbook:term_list')

class TermUpdate(LoginRequiredMixin, UpdateView):
    model = Term
    form_class = TermForm
    template_name = 'textbook/term_form.html'
    success_url = reverse_lazy('textbook:term_list')

class TermDelete(LoginRequiredMixin, DeleteView):
    model = Term
    success_url = reverse_lazy('textbook:term_list')

class TermList(LoginRequiredMixin, ListView):
    model = Term
    context_object_name = 'terms'
    template_name = 'textbook/term_list.html'

class WeekCreate(LoginRequiredMixin, CreateView):
    model = Week
    form_class = WeekForm
    template_name = 'textbook/week_form.html'
    success_url = reverse_lazy('textbook:week_list')

class WeekUpdate(LoginRequiredMixin, UpdateView):
    model = Week
    form_class = WeekForm
    template_name = 'textbook/week_form.html'
    success_url = reverse_lazy('textbook:week_list')

class WeekDelete(LoginRequiredMixin, DeleteView):
    model = Week
    success_url = reverse_lazy('textbook:week_list')

class WeekList(LoginRequiredMixin, ListView):
    model = Week
    context_object_name = 'weeks'
    template_name = 'textbook/week_list.html'

class SchoolCreate(LoginRequiredMixin, CreateView):
    model = School
    form_class = SchoolForm
    template_name = 'textbook/school_form.html'
    success_url = reverse_lazy('textbook:school_list')

class SchoolUpdate(LoginRequiredMixin, UpdateView):
    model = School
    form_class = SchoolForm
    template_name = 'textbook/school_form.html'
    success_url = reverse_lazy('textbook:school_list')

class SchoolDelete(LoginRequiredMixin, DeleteView):
    model = School
    success_url = reverse_lazy('textbook:school_list')

class SchoolList(LoginRequiredMixin, ListView):
    model = School
    context_object_name = 'schools'
    template_name = 'textbook/school_list.html'

class SubjectCreate(LoginRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'textbook/subject_form.html'
    success_url = reverse_lazy('textbook:subject_list')

class SubjectUpdate(LoginRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'textbook/subject_form.html'
    success_url = reverse_lazy('textbook:subject_list')

class SubjectDelete(LoginRequiredMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy('textbook:subject_list')

class SubjectList(LoginRequiredMixin, ListView):
    model = Subject
    context_object_name = 'subjects'
    template_name = 'textbook/subject_list.html'

class SyllabusTopicCreate(LoginRequiredMixin, CreateView):
    model = SyllabusTopic
    form_class = SyllabusTopicForm
    template_name = 'textbook/syllabus_topic_form.html'
    success_url = reverse_lazy('textbook:syllabus_topic_list')

class SyllabusTopicUpdate(LoginRequiredMixin, UpdateView):
    model = SyllabusTopic
    form_class = SyllabusTopicForm
    template_name = 'textbook/syllabus_topic_form.html'
    success_url = reverse_lazy('textbook:syllabus_topic_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:  # Check if there's an existing object being edited
            # Serialize selected_outcomes to JSON and mark as safe for HTML
            selected_outcomes = list(self.object.outcomes.values_list('id', flat=True))
            context['selected_outcomes'] = mark_safe(json.dumps(selected_outcomes))
        return context

class SyllabusTopicDelete(LoginRequiredMixin, DeleteView):
    model = SyllabusTopic
    success_url = reverse_lazy('textbook:syllabus_topic_list')

class SyllabusTopicList(LoginRequiredMixin, ListView):
    model = SyllabusTopic
    context_object_name = 'topics_by_subject'
    template_name = 'textbook/syllabus_topic_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topics = SyllabusTopic.objects.all().select_related('subject')
        topics_by_subject = defaultdict(list)
        for topic in topics:
            topics_by_subject[topic.subject].append(topic)
        context['topics_by_subject'] = dict(topics_by_subject)
        return context

class SyllabusOutcomeCreate(LoginRequiredMixin, CreateView):
    model = SyllabusOutcome
    form_class = SyllabusOutcomeForm
    template_name = 'textbook/syllabus_outcome_form.html'
    success_url = reverse_lazy('textbook:syllabus_outcome_list')

class SyllabusOutcomeUpdate(LoginRequiredMixin, UpdateView):
    model = SyllabusOutcome
    form_class = SyllabusOutcomeForm
    template_name = 'textbook/syllabus_outcome_form.html'
    success_url = reverse_lazy('textbook:syllabus_outcome_list')

class SyllabusOutcomeDelete(LoginRequiredMixin, DeleteView):
    model = SyllabusOutcome
    success_url = reverse_lazy('textbook:syllabus_outcome_list')

class SyllabusOutcomeList(LoginRequiredMixin, ListView):
    model = SyllabusOutcome
    context_object_name = 'outcomes_by_subject'
    template_name = 'textbook/syllabus_outcome_list.html'  
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Retrieve all outcomes and then group them by subject
        outcomes = SyllabusOutcome.objects.all().select_related('subject')
        outcomes_by_subject = defaultdict(list)
        for outcome in outcomes:
            outcomes_by_subject[outcome.subject].append(outcome)
        # Update the context with the grouped outcomes
        context['outcomes_by_subject'] = dict(outcomes_by_subject)
        return context
    
def outcomes_for_subject(request, subject_id):
    outcomes = SyllabusOutcome.objects.filter(subject_id=subject_id).values('id', 'outcome_number', 'outcome_description')
    return JsonResponse(list(outcomes), safe=False)

class SyllabusContentCreate(LoginRequiredMixin, CreateView):
    model = SyllabusContent
    form_class = SyllabusContentForm
    template_name = 'textbook/syllabus_content_form.html'
    success_url = reverse_lazy('textbook:syllabus_content_list')

class SyllabusContentUpdate(LoginRequiredMixin, UpdateView):
    model = SyllabusContent
    form_class = SyllabusContentForm
    template_name = 'textbook/syllabus_content_form.html'
    success_url = reverse_lazy('textbook:syllabus_content_list')

class SyllabusContentDelete(LoginRequiredMixin, DeleteView):
    model = SyllabusContent
    success_url = reverse_lazy('textbook:syllabus_content_list')

class SyllabusContentList(LoginRequiredMixin, ListView):
    model = SyllabusContent
    context_object_name = 'contents'
    template_name = 'textbook/syllabus_content_list.html'

class SyllabusIndicatorCreate(LoginRequiredMixin, CreateView):
    model = SyllabusIndicator
    form_class = SyllabusIndicatorForm
    template_name = 'textbook/syllabus_indicator_form.html'
    success_url = reverse_lazy('textbook:syllabus_indicator_list')

class SyllabusIndicatorUpdate(LoginRequiredMixin, UpdateView):
    model = SyllabusIndicator
    form_class = SyllabusIndicatorForm
    template_name = 'textbook/syllabus_indicator_form.html'
    success_url = reverse_lazy('textbook:syllabus_indicator_list')

class SyllabusIndicatorDelete(LoginRequiredMixin, DeleteView):
    model = SyllabusIndicator
    success_url = reverse_lazy('textbook:syllabus_indicator_list')

class SyllabusIndicatorList(LoginRequiredMixin, ListView):
    model = SyllabusIndicator
    context_object_name = 'indicators'
    template_name = 'textbook/syllabus_indicator_list.html'

