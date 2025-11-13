from django import forms
from .models import Subject, Course

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['course','subject_code','description']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'subject_code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }