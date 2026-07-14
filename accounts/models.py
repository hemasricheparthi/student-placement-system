"""
User authentication and core models for the placement portal.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Extended user model with role-based access control."""

    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        PLACEMENT_OFFICER = 'PLACEMENT_OFFICER', 'Placement Officer'
        STUDENT = 'STUDENT', 'Student'
        COMPANY = 'COMPANY', 'Company/Recruiter'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
    )
    phone = models.CharField(max_length=15, blank=True)
    is_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def is_placement_officer(self):
        return self.role == self.Role.PLACEMENT_OFFICER

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_company(self):
        return self.role == self.Role.COMPANY


class Department(models.Model):
    """Academic departments in the institution."""

    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    hod_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Skill(models.Model):
    """Skills database for matching and filtering."""

    class Category(models.TextChoices):
        TECHNICAL = 'TECHNICAL', 'Technical'
        SOFT = 'SOFT', 'Soft Skill'
        TOOL = 'TOOL', 'Tool/Framework'
        LANGUAGE = 'LANGUAGE', 'Programming Language'

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.TECHNICAL,
    )
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Notification(models.Model):
    """In-app notifications for users."""

    class NotificationType(models.TextChoices):
        INFO = 'INFO', 'Information'
        SUCCESS = 'SUCCESS', 'Success'
        WARNING = 'WARNING', 'Warning'
        APPLICATION = 'APPLICATION', 'Application Update'
        INTERVIEW = 'INTERVIEW', 'Interview'
        OFFER = 'OFFER', 'Offer'

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.INFO,
    )
    link = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class Announcement(models.Model):
    """System-wide announcements managed by admin/officers."""

    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='announcements',
    )
    is_active = models.BooleanField(default=True)
    target_roles = models.CharField(
        max_length=100,
        blank=True,
        help_text='Comma-separated roles: STUDENT,COMPANY,PLACEMENT_OFFICER',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
