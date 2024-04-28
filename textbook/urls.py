from django.urls import path
from . import views
from .views import QuestionCreate, QuestionUpdate, QuestionDelete, QuestionList
from .views import outcomes_for_subject
from .views import get_topics_by_subject
from .views import get_sequences_by_subject, get_terms_by_sequence, get_weeks_by_term, get_lessons_by_week, get_pages_by_lesson
from .views import LessonSchedule, StudyMaterials
from .views import TermCreate, TermUpdate, TermDelete, TermList
from .views import WeekCreate, WeekUpdate, WeekDelete, WeekList
from .views import SchoolCreate, SchoolUpdate, SchoolDelete, SchoolList
from .views import SubjectCreate, SubjectUpdate, SubjectDelete, SubjectList
from .views import SyllabusTopicCreate, SyllabusTopicUpdate, SyllabusTopicDelete, SyllabusTopicList
from .views import SyllabusOutcomeCreate, SyllabusOutcomeUpdate, SyllabusOutcomeDelete, SyllabusOutcomeList
from .views import SyllabusContentCreate, SyllabusContentUpdate, SyllabusContentDelete, SyllabusContentList
from .views import SyllabusIndicatorCreate, SyllabusIndicatorUpdate, SyllabusIndicatorDelete, SyllabusIndicatorList

urlpatterns = [
    path('', views.index, name='index'),
    path('lesson_schedule/', LessonSchedule.as_view(), name='lesson_schedule'),
    path('api/sequences/<int:subject_id>/', views.get_sequences_by_subject, name='get_sequences_by_subject'),
    path('api/terms/<int:sequence_id>/', views.get_terms_by_sequence, name='get_terms_by_sequence'),
    path('api/weeks/<int:term_id>/', views.get_weeks_by_term, name='get_weeks_by_term'),
    path('api/lessons/<int:week_id>/', views.get_lessons_by_week, name='get_lessons_by_week'),
    
    path('api/lessons/<int:lesson_id>/pages/', views.get_pages_by_lesson, name='lesson_pages'),
    path('api/pages/<int:page_id>/slides/', views.get_slides_by_page, name='page_slides'),

    path('study_materials/', StudyMaterials.as_view(), name='study_materials'),

    path('question/add/', QuestionCreate.as_view(), name='question_add'),
    path('question/<int:pk>/edit/', QuestionUpdate.as_view(), name='question_edit'),
    path('question/<int:pk>/delete/', QuestionDelete.as_view(), name='question_delete'),
    path('questions/', QuestionList.as_view(), name='question_list'),

    path('school/add/', SchoolCreate.as_view(), name='school_add'),
    path('school/<int:pk>/edit/', SchoolUpdate.as_view(), name='school_edit'),
    path('school/<int:pk>/delete/', SchoolDelete.as_view(), name='school_delete'),
    path('school/', SchoolList.as_view(), name='school_list'),

    path('subject/add/', SubjectCreate.as_view(), name='subject_add'),
    path('subject/<int:pk>/edit/', SubjectUpdate.as_view(), name='subject_edit'),
    path('subject/<int:pk>/delete/', SubjectDelete.as_view(), name='subject_delete'),
    path('subject/', SubjectList.as_view(), name='subject_list'),

    path('term/add/', TermCreate.as_view(), name='term_add'),
    path('term/<int:pk>/edit/', TermUpdate.as_view(), name='term_edit'),
    path('term/<int:pk>/delete/', TermDelete.as_view(), name='term_delete'),
    path('term/', TermList.as_view(), name='term_list'),

    path('week/add/', WeekCreate.as_view(), name='week_add'),
    path('week/<int:pk>/edit/', WeekUpdate.as_view(), name='week_edit'),
    path('week/<int:pk>/delete/', WeekDelete.as_view(), name='week_delete'),
    path('week/', WeekList.as_view(), name='week_list'),

    path('syllabus_topic/add/', SyllabusTopicCreate.as_view(), name='syllabus_topic_add'),
    path('syllabus_topic/<int:pk>/edit/', SyllabusTopicUpdate.as_view(), name='syllabus_topic_edit'),
    path('syllabus_topic/<int:pk>/delete/', SyllabusTopicDelete.as_view(), name='syllabus_topic_delete'),
    path('syllabus_topic/', SyllabusTopicList.as_view(), name='syllabus_topic_list'),
    path('topics/<int:subject_id>/', views.get_topics_by_subject, name='get_topics_by_subject'),

    path('syllabus_outcome/add/', SyllabusOutcomeCreate.as_view(), name='syllabus_outcome_add'),
    path('syllabus_outcome/<int:pk>/edit/', SyllabusOutcomeUpdate.as_view(), name='syllabus_outcome_edit'),
    path('syllabus_outcome/<int:pk>/delete/', SyllabusOutcomeDelete.as_view(), name='syllabus_outcome_delete'),
    path('syllabus_outcome/', SyllabusOutcomeList.as_view(), name='syllabus_outcome_list'),
    path('outcomes_for_subject/<int:subject_id>/', views.outcomes_for_subject, name='outcomes_for_subject'),
    

    path('syllabus_content/add/', SyllabusContentCreate.as_view(), name='syllabus_content_add'),
    path('syllabus_content/<int:pk>/edit/', SyllabusContentUpdate.as_view(), name='syllabus_content_edit'),
    path('syllabus_content/<int:pk>/delete/', SyllabusContentDelete.as_view(), name='syllabus_content_delete'),
    path('syllabus_content/', SyllabusContentList.as_view(), name='syllabus_content_list'),

    path('syllabus_indicator/add/', SyllabusIndicatorCreate.as_view(), name='syllabus_indicator_add'),
    path('syllabus_indicator/<int:pk>/edit/', SyllabusIndicatorUpdate.as_view(), name='syllabus_indicator_edit'),
    path('syllabus_indicator/<int:pk>/delete/', SyllabusIndicatorDelete.as_view(), name='syllabus_indicator_delete'),
    path('syllabus_indicator/', SyllabusIndicatorList.as_view(), name='syllabus_indicator_list'),
]