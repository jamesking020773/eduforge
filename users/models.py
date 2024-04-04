from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=[('school', 'School'), ('admin', 'Admin'), ('teacher', 'Teacher'), ('student', 'Student')])
    schools = models.ManyToManyField('textbook.School', blank=True) 
    subjects = models.ManyToManyField('textbook.Subject', blank=True)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    year_group = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.user.username
    
class StudentSubjectLink(models.Model):
    student = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='student_subjects')
    subject = models.ForeignKey('textbook.Subject', on_delete=models.CASCADE)
    teacher = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='teacher_subjects')
    class Meta:
        unique_together = ('student', 'subject', 'teacher')
    def __str__(self):
        return f"{self.student.user.username} - {self.subject.subjectName} - {self.teacher.user.username}"