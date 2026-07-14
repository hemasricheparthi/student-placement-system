"""Customized Django admin for placement portal."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import Announcement, CustomUser, Department, Notification, Skill
from companies.models import CompanyProfile
from jobs.models import Application, Job
from placement.models import Interview, OfferLetter, PlacementDrive
from students.models import Certification, Project, Resume, StudentProfile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_verified', 'is_active', 'created_at']
    list_filter = ['role', 'is_verified', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Placement Portal', {'fields': ('role', 'phone', 'is_verified', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Placement Portal', {'fields': ('role', 'phone')}),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'hod_name', 'is_active']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_by', 'created_at']


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['enrollment_no', 'user', 'department', 'cgpa', 'placement_status', 'is_profile_verified']
    list_filter = ['placement_status', 'department', 'is_profile_verified']
    filter_horizontal = ['skills']


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'student', 'issuing_organization', 'issue_date']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'student', 'technologies']


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['student', 'is_active', 'uploaded_at']


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'industry', 'is_verified', 'is_active']
    list_filter = ['is_verified', 'industry']


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'status', 'salary_package', 'last_date_to_apply']
    list_filter = ['status', 'job_type']
    filter_horizontal = ['required_skills', 'eligible_departments']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'job', 'status', 'match_percentage', 'applied_at']
    list_filter = ['status']


@admin.register(PlacementDrive)
class PlacementDriveAdmin(admin.ModelAdmin):
    list_display = ['title', 'drive_date', 'status']
    filter_horizontal = ['companies', 'departments']


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ['application', 'interview_type', 'scheduled_date', 'status']


@admin.register(OfferLetter)
class OfferLetterAdmin(admin.ModelAdmin):
    list_display = ['application', 'package_offered', 'status', 'issued_at']
