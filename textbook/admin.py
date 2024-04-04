from django.contrib import admin
from .models import School, Subject 
from .models import ExamQuestion
from .models import RevisionQuestion
from .models import CodeQuestion
from .models import ThinkingLevel
from .models import Textbook, TextbookTopic, TextbookSection, TextbookPage, TextbookSlide
from .models import SyllabusTopic, SyllabusOutcome, SyllabusContent, SyllabusIndicator
from .models import Sequence, Term, Week, Lesson

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name', 'learning_area', 'stage', 'year')  
    search_fields = ('subject_name', 'learning_area')  
    ordering = ('subject_name', 'year',)  

class SequenceAdmin(admin.ModelAdmin):
    list_display = ('sequence_year', 'sequence_name')   
    ordering = ('sequence_year', 'sequence_name') 
    
class TermAdmin(admin.ModelAdmin):
    list_display = ('term_number', 'term_year', 'term_start_date')
    ordering = ('term_start_date',)
    filter_horizontal = ('sequences',)

class WeekAdmin(admin.ModelAdmin):
    list_display = ('get_term_number', 'week_number', 'week_start_date')
    ordering = ('term', 'week_start_date',)
    def get_term_number(self, obj):
        return obj.term.term_number
    get_term_number.admin_order_field = 'term'  
    get_term_number.short_description = 'Term Number'  

class TextbookPageAdmin(admin.ModelAdmin):
    list_display = ('page_title', 'page_number')
    filter_horizontal = ('sections',)

class TextbookSlideAdmin(admin.ModelAdmin):
    list_display = ('slide_title', 'slide_number')
    filter_horizontal = ('pages',)

class LessonAdmin(admin.ModelAdmin):
    list_display = ('lesson_title', 'lesson_number')
    filter_horizontal = ('syllabus_content', 'syllabus_outcomes', 'pages',)

class AssessmentTaskAdmin(admin.ModelAdmin):
    list_display = ('assessment_number', 'assessment_title', 'due_date')
    filter_horizontal = ('syllabus_topics', 'syllabus_outcomes', 'assessment_sections',)
    ordering = ('assessment_number',)

class QuizAdmin(admin.ModelAdmin):
    list_display = ('quiz_title', 'quiz_start_date')
    filter_horizontal = ('syllabus_outcomes', 'revision_questions', 'exam_questions', 'code_questions')
    ordering = ('quiz_start_date',)

class CodeQuestionAdmin(admin.ModelAdmin):
    list_display = ('cq_question_title', 'cq_question_text')
    filter_horizontal = ('syllabus_outcomes',)

class RevisionQuestionAdmin(admin.ModelAdmin):
    list_display = ('rq_question_title', 'rq_question_text')
    filter_horizontal = ('syllabus_outcomes',)

class ExamQuestionAdmin(admin.ModelAdmin):
    list_display = ('eq_question_title', 'eq_question_text')
    filter_horizontal = ('syllabus_outcomes',)

admin.site.register(School)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(ExamQuestion, ExamQuestionAdmin)
admin.site.register(RevisionQuestion, RevisionQuestionAdmin)
admin.site.register(CodeQuestion, CodeQuestionAdmin)
admin.site.register(ThinkingLevel)
admin.site.register(TextbookPage, TextbookPageAdmin)
admin.site.register(TextbookSlide, TextbookSlideAdmin)
admin.site.register(Textbook)
admin.site.register(TextbookTopic)
admin.site.register(TextbookSection)
admin.site.register(SyllabusTopic)
admin.site.register(SyllabusOutcome)
admin.site.register(SyllabusContent)
admin.site.register(SyllabusIndicator)
admin.site.register(Sequence, SequenceAdmin)
admin.site.register(Term, TermAdmin)
admin.site.register(Week, WeekAdmin)
admin.site.register(Lesson, LessonAdmin)