"""
Job openings and application models.
"""
from django.db import models


class Job(models.Model):
    """Job opening posted by companies."""

    class JobType(models.TextChoices):
        FULL_TIME = 'FULL_TIME', 'Full Time'
        INTERNSHIP = 'INTERNSHIP', 'Internship'
        CONTRACT = 'CONTRACT', 'Contract'

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        OPEN = 'OPEN', 'Open'
        CLOSED = 'CLOSED', 'Closed'
        FILLED = 'FILLED', 'Filled'

    company = models.ForeignKey(
        'companies.CompanyProfile',
        on_delete=models.CASCADE,
        related_name='jobs',
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    job_type = models.CharField(
        max_length=20,
        choices=JobType.choices,
        default=JobType.FULL_TIME,
    )
    location = models.CharField(max_length=200)
    salary_package = models.CharField(max_length=100, help_text='e.g. 6-8 LPA')
    min_cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    max_backlogs = models.PositiveIntegerField(default=0)
    eligible_departments = models.ManyToManyField(
        'accounts.Department',
        blank=True,
        related_name='eligible_jobs',
    )
    required_skills = models.ManyToManyField(
        'accounts.Skill',
        related_name='required_for_jobs',
    )
    experience_required = models.CharField(max_length=100, default='Fresher')
    vacancies = models.PositiveIntegerField(default=1)
    last_date_to_apply = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
    )
    placement_drive = models.ForeignKey(
        'placement.PlacementDrive',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='jobs',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.company.company_name}"

    @property
    def is_open(self):
        from django.utils import timezone
        return (
            self.status == self.Status.OPEN
            and self.last_date_to_apply >= timezone.now().date()
        )


class Application(models.Model):
    """Student job application with resume match data."""

    class Status(models.TextChoices):
        APPLIED = 'APPLIED', 'Applied'
        SHORTLISTED = 'SHORTLISTED', 'Shortlisted'
        INTERVIEW_SCHEDULED = 'INTERVIEW_SCHEDULED', 'Interview Scheduled'
        SELECTED = 'SELECTED', 'Selected'
        REJECTED = 'REJECTED', 'Rejected'
        OFFERED = 'OFFERED', 'Offered'
        OFFER_ACCEPTED = 'OFFER_ACCEPTED', 'Offer Accepted'
        OFFER_REJECTED = 'OFFER_REJECTED', 'Offer Rejected'

    student = models.ForeignKey(
        'students.StudentProfile',
        on_delete=models.CASCADE,
        related_name='applications',
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications',
    )
    resume = models.ForeignKey(
        'students.Resume',
        on_delete=models.SET_NULL,
        null=True,
        related_name='applications',
    )
    status = models.CharField(
        max_length=25,
        choices=Status.choices,
        default=Status.APPLIED,
    )
    cover_letter = models.TextField(blank=True)
    match_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
    )
    matched_skills = models.JSONField(default=list, blank=True)
    missing_skills = models.JSONField(default=list, blank=True)
    suggested_skills = models.JSONField(default=list, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, help_text='Internal notes by company/officer')

    class Meta:
        ordering = ['-applied_at']
        unique_together = ['student', 'job']

    def __str__(self):
        return f"{self.student.enrollment_no} -> {self.job.title}"
