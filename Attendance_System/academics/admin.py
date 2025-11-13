from django.contrib import admin
from . models import(
    AssignedSubjects,
    Subject,
    Course
)
# Register your models here.
admin.site.register(AssignedSubjects)
admin.site.register(Subject)
admin.site.register(Course)