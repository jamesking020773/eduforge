from django import forms
from django.contrib.auth.models import User
from textbook.models import School, Subject 
from django.core.exceptions import ValidationError

class AdminCreationForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=30)
    surname = forms.CharField(label='Surname', max_length=150)
    email = forms.EmailField(label='Email')
    school_id = forms.ModelChoiceField(label='School', queryset=School.objects.all())
 
class TeacherCreationForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=30)
    surname = forms.CharField(label='Surname', max_length=150)
    email = forms.EmailField(label='Email')
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
