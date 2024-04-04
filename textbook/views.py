from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from users.models import UserProfile
from django.core import serializers
from django.shortcuts import render
from .models import ExamQuestion
from .forms import ExamQuestionForm
from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Subquery, Count
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

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
    template_name = 'textbook/question_confirm_delete.html'
    success_url = reverse_lazy('textbook:question_list')

class QuestionList(LoginRequiredMixin, ListView):
    model = ExamQuestion
    context_object_name = 'questions'
    template_name = 'textbook/question_list.html'