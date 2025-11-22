from django.shortcuts import render, redirect, get_object_or_404
from .models import TeacherProfile,StudentProfile
from .forms import TeacherProfileForm, TeacherUserForm,StudentUserForm,StudentProfileForm
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from academics.models import Semester, Subject, SubjectOffering

User = get_user_model()


# -------------------------------
# Teacher List / Dashboard
# -------------------------------
def manage_teacher(request):
    teachers = TeacherProfile.objects.select_related('user').all()
    # Provide empty forms so the add-teacher modal can render its input fields
    user_form = TeacherUserForm()
    profile_form = TeacherProfileForm()

    return render(request, 'dashboard/manageteacher.html', {
        'teachers': teachers,
        'user_form': user_form,
        'profile_form': profile_form,
        'active': 'teacher',
    })


# -------------------------------
# Add Teacher
# -------------------------------
def add_teacher(request):
    email = None
    password_generated = None

    if request.method == "POST":
        user_form = TeacherUserForm(request.POST)
        profile_form = TeacherProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Generate random password
            random_password = get_random_string(8)

            user = user_form.save(commit=False)
            user.set_password(random_password)
            user.first_login = True
            user.role = 'teacher'
            user.save()

            teacher = profile_form.save(commit=False)
            teacher.user = user
            teacher.save()

            email = user.email
            password_generated = random_password

            messages.success(request, f"Teacher created! Email: {email}, Password: {password_generated}")
            return redirect('accounts:manage_teacher')
    else:
        user_form = TeacherUserForm()
        profile_form = TeacherProfileForm()

    return render(request, 'dashboard/manageteacher.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'email': email,
        'password': password_generated,
        'active': 'teacher',
    })


# -------------------------------
# Edit Teacher
# -------------------------------
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(TeacherProfile, id=teacher_id)

    if request.method == "POST":
        user_form = TeacherUserForm(request.POST, instance=teacher.user)
        profile_form = TeacherProfileForm(request.POST, instance=teacher)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Teacher updated successfully.")
            return redirect('accounts:manage_teacher')
    else:
        user_form = TeacherUserForm(instance=teacher.user)
        profile_form = TeacherProfileForm(instance=teacher)

    return render(request, 'dashboard/manageteacher.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'teacher': teacher,
        'active': 'teacher',
    })


# -------------------------------
# Delete Teacher
# -------------------------------
@require_POST
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(TeacherProfile, id=teacher_id)
    teacher.user.delete()  # Delete both user and profile
    teacher.delete()
    messages.success(request, "Teacher deleted successfully.")
    return redirect('accounts:manage_teacher')

def manage_student(request):
    students = StudentProfile.objects.select_related('course').all()
    return render(request, 'dashboard/managestudents.html', {'students': students})


def add_student(request):
    semester = request.POST.get('semester', '1st')
    course = request.POST.get('course', None)
    year = request.POST.get('year', None)

    if request.method == 'POST':
        user_form = StudentUserForm(request.POST)
        student_form = StudentProfileForm(request.POST, semester=semester, course=course)

        if user_form.is_valid() and student_form.is_valid():
            # Create user
            user = user_form.save(commit=False)
            user.set_password(get_random_string(8))
            user.role = "student"
            user.first_login = True
            user.save()

            # Create student profile
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            student.subjects.set(request.POST.getlist('subjects'))

            return redirect('accounts:manage_student')

    else:
        user_form = StudentUserForm()
        student_form = StudentProfileForm(semester=semester, course=course)

    # Initial subjects for modal
    subjects = Subject.objects.filter(semester_number=semester)
    if course:
        subjects = subjects.filter(course_id=course)
    if year:
        subject_ids = SubjectOffering.objects.filter(year=year).values_list('subject_id', flat=True)
        subjects = subjects.filter(id__in=subject_ids)

    return render(request, 'dashboard/add_student.html', {
        'user_form': user_form,
        'student_form': student_form,
        'semester': semester,
        'subjects': subjects
    })

    

def load_subjects(request):
    semester = request.GET.get('semester')
    course_id = request.GET.get('course')
    year = request.GET.get('year')

    subjects = Subject.objects.all()

    if semester:
        subjects = subjects.filter(semester_number=semester)
    if course_id:
        subjects = subjects.filter(course_id=course_id)
    if year:
        # Only subjects that have offerings for this year
        subject_ids = SubjectOffering.objects.filter(year=year).values_list('subject_id', flat=True)
        subjects = subjects.filter(id__in=subject_ids)

    data = [{'id': s.id, 'subject_code': s.subject_code, 'name': s.name} for s in subjects]
    return JsonResponse({'subjects': data})









# Login
# -------------------------------
'''def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = None

        if user:
            auth_user = authenticate(request, username=user.username, password=password)
            if auth_user:
                login(request, auth_user)

                if auth_user.first_login:
                    return redirect('accounts:change_password_first_time')
                else:
                    if auth_user.role == 'admin':
                        return redirect('dashboard:dashboard_home')
                    elif auth_user.role == 'teacher':
                        return redirect('dashboard:teacher_home')
                    elif auth_user.role == 'student':
                        return redirect('dashboard:student_home')
            else:
                messages.error(request, "Incorrect password.")
        else:
            messages.error(request, "User with this email does not exist.")

    return render(request, 'accounts/login.html')'''

'''def change_password_first_time(request):
    if request.method == "POST":
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password and new_password == confirm_password:
            request.user.password = make_password(new_password)
            request.user.first_login = False
            request.user.save()
            messages.success(request, "Password changed successfully!")
            return redirect('dashboard:dashboard_home')
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'accounts/change_password.html')
'''
