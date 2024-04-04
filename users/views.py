import json
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from users.models import UserProfile
from textbook.models import Subject, School
from .forms import TeacherCreationForm
from .forms import AdminCreationForm
from django.http import JsonResponse
from users.models import StudentSubjectLink
from django.conf import settings  

# Default pages for users
@login_required
def index(request):
    schools_list = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            schools_list = user_profile.schools.all()  # Directly pass the queryset of schools
        except UserProfile.DoesNotExist:
            schools_list = None
    else:
        return HttpResponseRedirect(reverse("login"))
    context = {'schools_list': schools_list}
    return render(request, "users/user.html", context)

@login_required
def teacher_classes(request):
    schools_list = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            schools_list = user_profile.schools.all()  # Directly pass the queryset of schools
        except UserProfile.DoesNotExist:
            schools_list = None
    else:
        return HttpResponseRedirect(reverse("login"))
    context = {'schools_list': schools_list}
    return render(request, "users/teacher_classes.html", context)

@login_required
def teacher_subjects(request):
    schools_list = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            schools_list = user_profile.schools.all()  # Directly pass the queryset of schools
        except UserProfile.DoesNotExist:
            schools_list = None
    else:
        return HttpResponseRedirect(reverse("login"))
    context = {'schools_list': schools_list}
    return render(request, "users/teacher_subjects.html", context)

@login_required
def student_subjects(request):
    schools_list = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            schools_list = user_profile.schools.all()  # Directly pass the queryset of schools
        except UserProfile.DoesNotExist:
            schools_list = None
    else:
        return HttpResponseRedirect(reverse("login"))
    context = {'schools_list': schools_list}
    return render(request, "users/student_subjects.html", context)

def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect(settings.LOGOUT_REDIRECT_URL) 
    
@login_required
def create_admin(request):
    if request.method == "POST":
        form = AdminCreationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            school = form.cleaned_data['school_id']
            # Check if a user with this email already exists
            user, user_created = User.objects.get_or_create(email=email, defaults={'username': email, 'first_name': first_name, 'last_name': surname})
            if user_created:
                user.set_password("P@ssword!23")
                user.save()
            else:
                # If the user exists, update user details
                user.first_name = first_name
                user.surname = surname
                user.save()
            # Create or update UserProfile
            profile, _ = UserProfile.objects.get_or_create(user=user, defaults={'user_type': 'admin'})
            profile.first_name = first_name
            profile.surname = surname
            profile.email = email
            profile.user_type = 'admin'
            profile.save()
            # Associate the user with the selected school
            if school not in profile.schools.all():
                profile.schools.add(school)
            messages.success(request, "Admin account successfully created.")
            return redirect('users:index')
    else:
        form = AdminCreationForm()
    return render(request, 'users/create_admin.html', {'form': form})

@login_required
def create_teacher(request):
    admin_profile = request.user.userprofile
    if admin_profile.user_type != 'admin':
        messages.error(request, "Action not Authorised")
        return redirect(settings.LOGIN_URL) 

    if request.method == 'POST':
        form = TeacherCreationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            subjects = form.cleaned_data['subjects']

            # Create or get the user with the provided email
            teacher_user, created = User.objects.get_or_create(
                email=email,
                defaults={'username': email, 'first_name': first_name, 'last_name': surname}
            )

            if created:
                # Consider a more secure approach for initial passwords
                teacher_user.set_password('P@ssword!23')
                teacher_user.save()

            # Create or update the UserProfile for the teacher
            teacher_profile, profile_created = UserProfile.objects.update_or_create(
                user=teacher_user,
                defaults={'first_name': first_name, 'surname': surname, 'email': email, 'user_type': 'teacher'}
            )

            # Link the teacher to the same schools as the admin
            for school in admin_profile.schools.all():
                teacher_profile.schools.add(school)

            # Add subjects to the teacher profile
            for subject in subjects:
                teacher_profile.subjects.add(subject)

            messages.success(request, "Teacher account {} successfully.".format("created" if created else "updated"))
            return redirect('users:index')
    else:
        form = TeacherCreationForm()
    return render(request, 'users/create_teacher.html', {'form': form})

def is_valid_email(email):
    # Simple regex for validating an email address
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(email_regex, email)

def get_subjects(request):
    learning_area = request.GET.get('learning_area')
    stage = request.GET.get('stage')
    subjects = Subject.objects.filter(learning_area=learning_area, stage=stage).values_list('id', 'subject_name')
    return JsonResponse(list(subjects), safe=False)

def create_student(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        surname = request.POST['surname']
        email = request.POST['email']
        subject_id = request.POST['subject']
        
        # Check if a user with the provided email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return redirect(settings.LOGIN_URL) 

        # Create user and user profile
        user = User.objects.create_user(username=email, email=email)
        user.set_unusable_password()  # Set an unusable password
        user.save()
        
        subject = Subject.objects.get(id=subject_id)
        user_profile = UserProfile.objects.create(
            user=user, first_name=first_name, surname=surname, email=email, user_type='student'
        )
        user_profile.subjects.add(subject)
        
        # Automatically log the user in after account creation
        login(request, user)
        
        return redirect('users:user')  

    else:
        subjects = Subject.objects.all()
        return render(request, 'users/create_student.html', {'subjects': subjects})

def is_first_row_header(column_data):
    header_keywords = ["first", "given", "name", "second", "surname", "last", "email"]
    # Ensure there's data to check
    if not column_data:
        return False
    first_item = column_data[0].lower() # Convert to lowercase to ensure case-insensitive comparison
    # Avoid names by adding space at the beginning and end
    if (f" {first_item}" in header_keywords) or (f"{first_item} " in header_keywords):
        return True
    # Additional check if the first row itself, without extra spaces
    if first_item in header_keywords:
        return True
    return False

@login_required
def bulk_import_students(request):
    teacher_profile = request.user.userprofile
    schools = teacher_profile.schools.all()  
    year_groups = ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
    subjects = Subject.objects.all()

    if request.method == "POST":
        school_id = request.POST.get('school')
        try:
            selected_school = schools.get(id=school_id)  
        except School.DoesNotExist:
            messages.error(request, "Invalid school selected.")
            return render(request, 'users/bulk_import_students.html', {
                'schools': schools,
                'subjects': subjects,
                'subject_name': subject_name,
                'year_groups': year_groups,  
                'year_group': year_group,
                'first_names': request.POST.get('first_names'),
                'surnames': request.POST.get('surnames'),
                'emails': request.POST.get('emails'),
            })
        year_group = request.POST.get('year_group')
        subject_name = request.POST.get('subject')
        first_names_raw = request.POST.get('first_names').splitlines()
        surnames_raw = request.POST.get('surnames').splitlines()
        emails_raw = request.POST.get('emails').splitlines()
        
        # Check if the first row in any of the columns is a header
        if (is_first_row_header(first_names_raw) or
                is_first_row_header(surnames_raw) or
                is_first_row_header(emails_raw)):
            # Exclude the first row if any column's first row is a header
            first_names = first_names_raw[1:] if is_first_row_header(first_names_raw) else first_names_raw
            surnames = surnames_raw[1:] if is_first_row_header(surnames_raw) else surnames_raw
            emails = emails_raw[1:] if is_first_row_header(emails_raw) else emails_raw
        else:
            # If no headers are detected, process all rows as data
            first_names, surnames, emails = first_names_raw, surnames_raw, emails_raw

        # Validate email addresses
        for email in emails:
            if not is_valid_email(email):
                messages.error(request, "Invalid email address detected.")
                # Return to the bulk_import_student page with the entered data retained
                return render(request, 'users/bulk_import_students.html', {
                'subjects': subjects,
                'schools': schools, 
                'subject_name': subject_name,
                'year_groups': year_groups,  
                'year_group': year_group,
                'first_names': request.POST.get('first_names'),
                'surnames': request.POST.get('surnames'),
                'emails': request.POST.get('emails'),
            })

        # Check if the number of rows match
        if not (len(first_names) == len(surnames) == len(emails)):
            messages.error(request, "The number of rows of data provided in each column do not match.")
            # Repopulate subjects for dropdown and retain input data
            return render(request, 'users/bulk_import_students.html', {
                'subjects': subjects,
                'schools': schools, 
                'subject_name': subject_name,
                'year_groups': year_groups,  
                'year_group': year_group,
                'first_names': request.POST.get('first_names'),
                'surnames': request.POST.get('surnames'),
                'emails': request.POST.get('emails'),
            })

        # When checking for a subject match, find by name instead of ID
        try:
            subject = Subject.objects.get(subjectName=subject_name)
        except Subject.DoesNotExist:
            messages.error(request, "Selected subject does not exist.")
            return redirect('users:bulk_import_students')

        # Combine the data into a list of dictionaries for display
        combined_data = [
            {'first_name': fn, 'surname': sn, 'email': em, 'year_group': year_group, 'subject': subject.subjectName,}
            for fn, sn, em in zip(first_names, surnames, emails)
        ]

        # Render a summary page with combined data
        combined_data_json = json.dumps(combined_data)
        return render(request, 'users/verify_import.html', {
            'combined_data_json': combined_data_json,
            'year_group': year_group,
            'subject_name': subject.subjectName,
            'school':selected_school,
        })

    else:
        # Render the form page for GET request
        return render(request, 'users/bulk_import_students.html', {
            'subjects': subjects,
            'year_groups': year_groups,  # Pass year groups to the template
            'schools': schools, 
        })
    
@login_required
def process_student_import(request):
    if request.method == "POST":
        year_group = request.POST.get('year_group')
        subject_name = request.POST.get('subject_name')
        import_data_str = request.POST.get('import_data', '')  # Get JSON string
        school_id = request.POST.get('school_id')

        if not import_data_str:
            messages.error(request, "No imported data provided.")
            return redirect('users:bulk_import_students')
    
        try:
            import_data = json.loads(import_data_str)  # Deserialize JSON
            subject = Subject.objects.get(subjectName=subject_name)
            school = School.objects.get(id=school_id)  # Retrieve the selected school
        except json.JSONDecodeError as e:
            messages.error(request, f"Invalid format of imported data: {str(e)}")
            return redirect('users:bulk_import_students')

        teacher_profile = request.user.userprofile

        for row in import_data:
            email = row.get('email')
            first_name = row.get('first_name')
            surname = row.get('surname')

            # Create or get the User instance
            user, created = User.objects.get_or_create(
                email=email,
                defaults={'username': email, 'first_name': first_name, 'last_name': surname}
            )

            if created:  # Only set the default password if the user was newly created
                user.set_password("P@ssword!23")
                user.save()

            # Update or create the UserProfile instance
            student_profile, profile_created = UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'first_name': first_name,
                    'surname': surname,
                    'email': email,
                    'user_type': 'student',
                    'year_group': year_group,
                }
            )

            student_profile.schools.add(school)  # Add the school to the student's profile
            student_profile.subjects.add(subject)  # Add the subject to the student's profile

            # Additionally, create or update a StudentSubjectLink to record the teacher-student-subject relationship
            StudentSubjectLink.objects.update_or_create(
                student=student_profile,
                subject=subject,
                teacher=teacher_profile
            )

        messages.success(request, "Bulk Student Import Successful")
        return redirect('users:index')
    else:
        return redirect('users:bulk_import_students')
    
@login_required
def delete_student_subject(request, student_id, subject_id):
    if request.method == "POST":
        student_profile = get_object_or_404(UserProfile, id=student_id, user_type='student')
        subject = get_object_or_404(Subject, id=subject_id)
        teacher_profile = request.user.userprofile
        # Ensure the teacher is authorised to delete this link
        StudentSubjectLink.objects.filter(student=student_profile, subject=subject, teacher=teacher_profile).delete()
        return redirect('users:modify_student')
    else:
        # Redirect or show an error if the request method is not POST
        return redirect('users:modify_student')
    
@login_required
def modify_student(request):
    # Ensure the user is a teacher
    if not request.user.userprofile.user_type == 'teacher':
        messages.error(request, "Action not Authorised")
        return redirect(settings.LOGIN_URL) 

    teacher_profile = request.user.userprofile
    # Fetch all StudentSubjectLinks for this teacher, including student and subject information
    links = StudentSubjectLink.objects.filter(teacher=teacher_profile).select_related('student', 'subject', 'student__user').prefetch_related('student__schools')
    # Organize students by school and then by subject
    schools_dict = {}
    for link in links:
        for school in link.student.schools.all():
            if school not in schools_dict:
                schools_dict[school] = {}
            if link.subject not in schools_dict[school]:
                schools_dict[school][link.subject] = []
            schools_dict[school][link.subject].append(link.student)

    # Convert dict to list of tuples for template context
    schools = [(school, subjects.items()) for school, subjects in schools_dict.items()]
    schools_list = teacher_profile.schools.all()
    return render(request, 'users/modify_student.html', {
        'schools': schools,  
        'schools_list': schools_list, 
    })