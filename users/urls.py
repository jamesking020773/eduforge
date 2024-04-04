from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("logout", views.logout_view, name="logout"),
    path("create_admin", views.create_admin, name="create_admin"),

    path('create_teacher', views.create_teacher, name='create_teacher'),
    path('teacher_classes', views.teacher_classes, name='teacher_classes'),
    path('teacher_subjects', views.teacher_subjects, name='teacher_subjects'),

    path('create_student', views.create_student, name='create_student'),
    path('modify_student', views.modify_student, name='modify_student'),
    path('student_subjects', views.student_subjects, name='student_subjects'),

    path('delete_student_subject/<int:student_id>/<int:subject_id>/', views.delete_student_subject, name='delete_student_subject'),
    path('get-subjects/', views.get_subjects, name='get_subjects'),
    path('bulk_import_students', views.bulk_import_students, name='bulk_import_students'),
    path('process_student_import', views.process_student_import, name='process_student_import'),
]