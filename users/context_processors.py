def schools_list_processor(request):
    if not request.user.is_authenticated:
        return {}

    # Retrieve the user profile
    user_profile = request.user.userprofile

    # Check if user is a teacher or student and fetch schools accordingly
    if user_profile.user_type == 'teacher':
        schools_list = user_profile.schools.all()
    elif user_profile.user_type == 'student':
        # Assuming students are also linked to schools in a similar way as teachers
        schools_list = user_profile.schools.all()
    else:
        schools_list = []

    return {'schools_list': schools_list}