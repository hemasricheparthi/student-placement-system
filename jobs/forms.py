"""Job and application forms."""
from django import forms

from accounts.models import Department, Skill
from jobs.models import Application, Job


class JobForm(forms.ModelForm):
    required_skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    eligible_departments = forms.ModelMultipleChoiceField(
        queryset=Department.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Job
        fields = [
            'title', 'description', 'job_type', 'location', 'salary_package',
            'min_cgpa', 'max_backlogs', 'eligible_departments', 'required_skills',
            'experience_required', 'vacancies', 'last_date_to_apply', 'status',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'salary_package': forms.TextInput(attrs={'class': 'form-control'}),
            'min_cgpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'max_backlogs': forms.NumberInput(attrs={'class': 'form-control'}),
            'experience_required': forms.TextInput(attrs={'class': 'form-control'}),
            'vacancies': forms.NumberInput(attrs={'class': 'form-control'}),
            'last_date_to_apply': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 4,
                'placeholder': 'Optional cover letter...',
            }),
        }


class JobSearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Search jobs...',
    }))
    company = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Company name',
    }))
    min_cgpa = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'placeholder': 'Min CGPA', 'step': '0.01',
    }))
    skill = forms.ModelChoiceField(
        queryset=Skill.objects.all(), required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    job_type = forms.ChoiceField(
        choices=[('', 'All Types')] + list(Job.JobType.choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
