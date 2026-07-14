"""Placement drive, interview, and offer forms."""
from django import forms

from accounts.models import Department
from companies.models import CompanyProfile
from placement.models import Interview, OfferLetter, PlacementDrive


class PlacementDriveForm(forms.ModelForm):
    companies = forms.ModelMultipleChoiceField(
        queryset=CompanyProfile.objects.filter(is_active=True, is_verified=True),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    departments = forms.ModelMultipleChoiceField(
        queryset=Department.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = PlacementDrive
        fields = [
            'title', 'description', 'drive_date', 'registration_deadline',
            'venue', 'companies', 'departments', 'min_cgpa', 'status',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'drive_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'registration_deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'venue': forms.TextInput(attrs={'class': 'form-control'}),
            'min_cgpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = [
            'interview_type', 'scheduled_date', 'duration_minutes',
            'venue', 'meeting_link', 'interviewer_name', 'status',
        ]
        widgets = {
            'scheduled_date': forms.DateTimeInput(attrs={
                'class': 'form-control', 'type': 'datetime-local',
            }),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'venue': forms.TextInput(attrs={'class': 'form-control'}),
            'meeting_link': forms.URLInput(attrs={'class': 'form-control'}),
            'interviewer_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class OfferLetterForm(forms.ModelForm):
    class Meta:
        model = OfferLetter
        fields = ['package_offered', 'joining_date', 'offer_details', 'file', 'response_deadline']
        widgets = {
            'package_offered': forms.TextInput(attrs={'class': 'form-control'}),
            'joining_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'offer_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'response_deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class InterviewFeedbackForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['feedback', 'rating', 'status']
        widgets = {
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
        }
