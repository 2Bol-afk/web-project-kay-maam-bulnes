from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.constants import YEAR_LEVEL_CHOICES, SECTION_CHOICES

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
    )

    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.username} ({self.role})"


class ParentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'parent'})
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    student_ID = models.CharField(primary_key=True, max_length=10)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)

    # Correctly reference Subject using a string
    subjects = models.ManyToManyField(
        "academics.Subject",
        related_name='students',
        blank=True
    )

    course = models.ForeignKey("academics.Course", on_delete=models.SET_NULL, null=True)
    parents = models.ManyToManyField(ParentProfile, related_name='students', blank=True)
    
    year = models.CharField(max_length=10, choices=YEAR_LEVEL_CHOICES)
    section = models.CharField(max_length=5, choices=SECTION_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.course.name if self.course else 'No Course'}"



class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    course = models.ForeignKey("academics.Course", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.course.name if self.course else 'No Course'}"
