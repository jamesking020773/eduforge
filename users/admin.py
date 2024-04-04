from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'get_schools', 'get_subjects', 'firstname', 'surname', 'email', 'year_group')
    list_filter = ('user_type', 'schools', 'subjects')
    search_fields = ('user__username', 'firstname', 'surname', 'email')

    # Adding filter_horizontal to manage ManyToManyField for schools
    filter_horizontal = ('schools', 'subjects')

    def get_schools(self, obj):
        return ", ".join([school.school_name for school in obj.schools.all()])
    get_schools.short_description = 'Schools'

    def get_subjects(self, obj):
        return ", ".join([subject.subject_name for subject in obj.subjects.all()])
    get_subjects.short_description = 'Subjects'

admin.site.register(UserProfile, UserProfileAdmin)