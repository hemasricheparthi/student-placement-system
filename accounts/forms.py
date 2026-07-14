"""
Authentication forms for all user roles.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm

from accounts.models import CustomUser, Department, Skill
from companies.models import CompanyProfile
from students.models import StudentProfile


class StudentRegistrationForm(UserCreationForm):
    """Student registration with profile fields."""

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=15, required=True)
    enrollment_no = forms.CharField(max_length=20, required=True)
    department = forms.ModelChoiceField(queryset=Department.objects.filter(is_active=True))
    batch_year = forms.IntegerField(min_value=2020, max_value=2030, initial=2026)
    cgpa = forms.DecimalField(min_value=0, max_value=10, decimal_places=2, initial=0)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'first_name', 'last_name', 'phone',
            'password1', 'password2',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.role = CustomUser.Role.STUDENT
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                enrollment_no=self.cleaned_data['enrollment_no'],
                department=self.cleaned_data['department'],
                batch_year=self.cleaned_data['batch_year'],
                cgpa=self.cleaned_data['cgpa'],
            )
        return user


class CompanyRegistrationForm(UserCreationForm):
    """Company/recruiter registration."""

    email = forms.EmailField(required=True)
    company_name = forms.CharField(max_length=200, required=True)
    industry = forms.CharField(max_length=100, required=True)
    contact_person = forms.CharField(max_length=100, required=True)
    contact_email = forms.EmailField(required=True)
    contact_phone = forms.CharField(max_length=15, required=True)
    website = forms.URLField(required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = CustomUser.Role.COMPANY
        if commit:
            user.save()
            CompanyProfile.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                industry=self.cleaned_data['industry'],
                contact_person=self.cleaned_data['contact_person'],
                contact_email=self.cleaned_data['contact_email'],
                contact_phone=self.cleaned_data['contact_phone'],
                website=self.cleaned_data.get('website', ''),
                description=self.cleaned_data.get('description', ''),
            )
        return user


class CustomLoginForm(AuthenticationForm):
    """Styled login form."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        })
    )


class ProfileUpdateForm(forms.ModelForm):
    """Update user profile information."""

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description', 'hod_name', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'hod_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'category', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        from accounts.models import Announcement
        model = Announcement
        fields = ['title', 'content', 'is_active', 'target_roles']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'target_roles': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'STUDENT,COMPANY,PLACEMENT_OFFICER',
            }),
        }
