from django.db import models
from accounts.constants import YEAR_LEVEL_CHOICES, SECTION_CHOICES

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.description}"


class Subject(models.Model):
    course = models.ForeignKey(Course,on_delete=models.SET_NULL, null=True)
    subject_code = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.course} - {self.subject_code}"


class AssignedSubjects(models.Model):
    teacher = models.ForeignKey("accounts.TeacherProfile", on_delete=models.CASCADE, related_name='assigned_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assigned_subjects')
    section = models.CharField(max_length=10, choices=SECTION_CHOICES)
    year = models.CharField(max_length=10, choices=YEAR_LEVEL_CHOICES)
    school_year = models.CharField(max_length=20)
    semester = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.teacher.user.last_name} - {self.subject.subject_code} - {self.year} - {self.section}"
