from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout
)

from django.contrib.auth.decorators import login_required

from .models import (
    Profile,
    Task,
    Subject,
    SavedNote
)


# ================= WELCOME =================

def welcome(request):

    return render(request, 'welcome.html')


# ================= LOGIN =================

def login_view(request):

    errors = {}

    if request.method == "POST":

        email = request.POST.get('email')

        password = request.POST.get('password')

        # EMAIL VALIDATION

        if not email:

            errors['email'] = "Email is required"

        # PASSWORD VALIDATION

        if not password:

            errors['password'] = "Password is required"

        # IF NO ERRORS

        if not errors:

            # CHECK USER EXISTS

            user_obj = User.objects.filter(
                email=email
            ).first()

            if not user_obj:

                errors['email'] = "User is not registered"

            else:

                # AUTHENTICATE USER

                user = authenticate(
                    request,
                    username=user_obj.username,
                    password=password
                )

                if user:

                    auth_login(request, user)

                    return redirect('dashboard')

                else:

                    errors['password'] = "Incorrect password"

    return render(request, 'login.html', {

        'errors': errors

    })


# ================= REGISTER =================

def register(request):

    errors = {}

    if request.method == "POST":

        name = request.POST.get('name')

        email = request.POST.get('email')

        password = request.POST.get('password')

        confirm_password = request.POST.get(
            'confirm_password'
        )

        field = request.POST.get('field')

        # VALIDATIONS

        if not name:

            errors['name'] = "Name is required"

        if not email:

            errors['email'] = "Email is required"

        if password != confirm_password:

            errors['confirm_password'] = (
                "Passwords do not match"
            )

        if len(password) < 6:

            errors['password'] = (
                "Password must be at least 6 characters"
            )

        if User.objects.filter(
            username=name
        ).exists():

            errors['name'] = (
                "Username already exists"
            )

        if User.objects.filter(
            email=email
        ).exists():

            errors['email'] = (
                "Email already registered"
            )

        # IF ERRORS

        if errors:

            return render(request, 'register.html', {

                'errors': errors

            })

        # CREATE USER

        user = User.objects.create_user(

            username=name,

            email=email,

            password=password
        )

        # CREATE PROFILE

        Profile.objects.create(

            user=user,

            field=field
        )

        return redirect('/login/')

    return render(request, 'register.html')


# ================= DASHBOARD =================

@login_required(login_url='/login/')
def dashboard(request):

    # CURRENT ACTIVE SECTION

    active_section = request.GET.get(
        'section',
        'dashboard'
    )

    # ================= POST REQUESTS =================

    if request.method == "POST":

        # CURRENT SECTION

        section = request.POST.get(
            'current_section',
            'dashboard'
        )

        # ================= ADD TASK =================

        if "add_task" in request.POST:

            task_title = request.POST.get("task")

            if task_title:

                Task.objects.create(

                    user=request.user,

                    title=task_title
                )

        # ================= COMPLETE TASK =================

        if "complete_task" in request.POST:

            task = Task.objects.get(

                id=request.POST.get(
                    "complete_task"
                ),

                user=request.user
            )

            task.completed = True

            task.save()

        # ================= DELETE TASK =================

        if "delete_task" in request.POST:

            Task.objects.filter(

                id=request.POST.get(
                    "delete_task"
                ),

                user=request.user

            ).delete()

        # ================= SAVE NOTE =================

        if "save_note" in request.POST:

            title = request.POST.get("title")

            note_link = request.POST.get(
                "note_link"
            )

            if title and note_link:

                SavedNote.objects.create(

                    user=request.user,

                    title=title,

                    note_link=note_link
                )

        # ================= DELETE NOTE =================

        if "delete_note" in request.POST:

            SavedNote.objects.filter(

                id=request.POST.get(
                    "delete_note"
                ),

                user=request.user

            ).delete()

        # ================= ADD SUBJECT =================

        if "add_subject" in request.POST:

            subject_name = request.POST.get(
                "subject"
            )

            if subject_name:

                Subject.objects.create(

                    user=request.user,

                    name=subject_name
                )

        # ================= DELETE SUBJECT =================

        if "delete_subject" in request.POST:

            Subject.objects.filter(

                id=request.POST.get(
                    "delete_subject"
                ),

                user=request.user

            ).delete()

        # REDIRECT SAME SECTION

        return redirect(
            f'/dashboard/?section={section}'
        )

    # ================= FETCH DATA =================

    user = request.user

    profile = Profile.objects.filter(
        user=user
    ).first()

    tasks = Task.objects.filter(
        user=user
    ).order_by('-created_at')

    notes = SavedNote.objects.filter(
        user=user
    ).order_by('-created_at')

    subjects = Subject.objects.filter(
        user=user
    ).order_by('-created_at')

    total_tasks = tasks.count()

    completed_tasks = tasks.filter(
        completed=True
    ).count()

    pending_tasks = (
        total_tasks - completed_tasks
    )

    return render(request, 'dashboard.html', {

        'user': user,

        'profile': profile,

        'tasks': tasks,

        'notes': notes,

        'subjects': subjects,

        'total_tasks': total_tasks,

        'completed_tasks': completed_tasks,

        'pending_tasks': pending_tasks,

        'active_section': active_section
    })


# ================= LOGOUT =================

def logout_view(request):

    logout(request)

    return redirect('/')