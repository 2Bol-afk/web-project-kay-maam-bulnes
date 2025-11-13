from django.shortcuts import render, redirect

# Create your views here.
def admin_dashboard(request):
    return render(request, 'dashboard/admindashboard.html')


def manage_student(request):
    return render(request, 'dashboard/managestudents.html')

