from django.urls import path
from . import views
app_name = 'accounts'
urlpatterns = [
    path("teachers/", views.manage_teacher, name="manage_teacher"),
    path("teachers/add/", views.add_teacher, name="add_teacher"),
    path("teachers/<int:teacher_id>/edit/", views.edit_teacher, name="edit_teacher"),
    path("teachers/<int:teacher_id>/delete/", views.delete_teacher, name="delete_teacher"),
    path('student/',views.manage_student,name='manage_student'),
    path('students/add/',views.add_student,name='add_student'),
    path('ajax/load-subjects/', views.load_subjects, name='load_subjects'),
]
