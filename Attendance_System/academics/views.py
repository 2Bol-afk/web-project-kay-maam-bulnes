from django.shortcuts import render, redirect,get_object_or_404
from .forms import SubjectForm
from .models import Subject,Course


def manage_subject(request):
    subjects = Subject.objects.all()
    courses = Course.objects.all()

    if request.method == 'POST' and 'add_subject' in request.POST:
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('academics:manage_subjects')
    elif request.method == 'POST' and 'edit_subject' in request.POST:
        subjectID= request.POST.get('subject_id')
        subject = get_object_or_404(Subject,id=subjectID)
        form = SubjectForm(request.POST,instance=subject)
        if form.is_valid():
            form.save()
            return redirect('academics:manage_subjects')
        
    elif request.method == 'POST' and 'delete_subject' in request.POST:
        subjectID = request.POST.get('subject_id')
        subject = get_object_or_404(Subject, id=subjectID)
        subject.delete()
        return redirect('academics:manage_subjects')

    add_form = SubjectForm()

    return render(request, 'dashboard/managesubjects.html', {
        'subjects': subjects, 
        'add_form': add_form,
        'courses':courses
        })