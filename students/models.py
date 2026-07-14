"""
Student profile and academic models.
"""
from django.conf import settings
from django.db import models


class StudentProfile(models.Model):
    """Complete student profile with academic and placement details."""

    class PlacementStatus(models.TextChoices):
        UNPLACED = 'UNPLACED', 'Unplaced'
        APPLIED = 'APPLIED', 'Applied'
        SHORTLISTED = 'SHORTLISTED', 'Shortlisted'
        INTERVIEWED = 'INTERVIEWED', 'Interviewed'
        OFFERED = 'OFFERED', 'Offered'
        PLACED = 'PLACED', 'Placed'
        REJECTED = 'REJECTED', 'Rejected'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile',
    )
    enrollment_no = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(
        'accounts.Department',
        on_delete=models.SET_NULL,
        null=True,
        related_name='students',
    )
    batch_year = models.PositiveIntegerField(default=2026)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    backlogs = models.PositiveIntegerField(default=0)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    skills = models.ManyToManyField(
        'accounts.Skill',
        blank=True,
        related_name='students',
    )
    placement_status = models.CharField(
        max_length=20,
        choices=PlacementStatus.choices,
        default=PlacementStatus.UNPLACED,
    )
    is_profile_verified = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.enrollment_no}"

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username


class Certification(models.Model):
    """Student certifications."""

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='certifications',
    )
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_url = models.URLField(blank=True)

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.name} - {self.student.enrollment_no}"


class Project(models.Model):
    """Student projects portfolio."""

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='projects',
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=300)
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} - {self.student.enrollment_no}"


class Resume(models.Model):
    """Student resume uploads with extracted text for matching."""

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='resumes',
    )
    file = models.FileField(upload_to='resumes/')
    extracted_text = models.TextField(blank=True)
    extracted_skills = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Resume - {self.student.enrollment_no} ({self.uploaded_at.date()})"
