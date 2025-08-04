# School/forms.py
from django import forms
from .models import Attendance, Result

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('date', 'subject', 'student', 'status')
        widgets = {
            'date': forms.SelectDateWidget(),  # fixed: added parentheses
        }

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ('student', 'subject', 'marks', 'term')
