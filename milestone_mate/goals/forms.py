from django import forms
from .models import Goal

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['name', 'description', 'goal_type', 'target_date', 'attachment']
        widgets = {
            'goal_type': forms.Select(attrs={'id': 'goal_type', 'onchange': 'toggleDateField()'}),
            'target_date': forms.DateInput(attrs={'type': 'date', 'id': 'target_date_field'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
