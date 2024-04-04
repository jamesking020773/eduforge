def schools_list_processor(request):
    if not request.user.is_authenticated:
        return {}

    # Assuming the UserProfile model has a `schools` relationship
    teacher_profile = request.user.userprofile
    schools_list = teacher_profile.schools.all() if teacher_profile.user_type == 'teacher' else []
    
    return {'schools_list': schools_list}