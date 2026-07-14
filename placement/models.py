"""
Placement drives, interviews, and offer letter models.
"""
from django.db import models


class PlacementDrive(models.Model):
    """Campus placement drive events."""

    class Status(models.TextChoices):
        UPCOMING = 'UPCOMING', 'Upcoming'
        ONGOING = 'ONGOING', 'Ongoing'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    drive_date = models.DateField()
    registration_deadline = models.DateField()
    venue = models.CharField(max_length=200, blank=True)
    companies = models.ManyToManyField(
        'companies.CompanyProfile',
        blank=True,
        related_name='placement_drives',
    )
    departments = models.ManyToManyField(
        'accounts.Department',
        blank=True,
        related_name='placement_drives',
    )
    min_cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.UPCOMING,
    )
    created_by = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_drives',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['drive_date']

    def __str__(self):
        return f"{self.title} ({self.drive_date})"


class Interview(models.Model):
    """Interview scheduling for shortlisted candidates."""

    class InterviewType(models.TextChoices):
        TECHNICAL = 'TECHNICAL', 'Technical'
        HR = 'HR', 'HR'
        GROUP_DISCUSSION = 'GD', 'Group Discussion'
        APTITUDE = 'APTITUDE', 'Aptitude Test'
        FINAL = 'FINAL', 'Final Round'

    class Status(models.TextChoices):
        SCHEDULED = 'SCHEDULED', 'Scheduled'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        RESCHEDULED = 'RESCHEDULED', 'Rescheduled'

    application = models.ForeignKey(
        'jobs.Application',
        on_delete=models.CASCADE,
        related_name='interviews',
    )
    interview_type = models.CharField(
        max_length=20,
        choices=InterviewType.choices,
        default=InterviewType.TECHNICAL,
    )
    scheduled_date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    venue = models.CharField(max_length=200, blank=True)
    meeting_link = models.URLField(blank=True)
    interviewer_name = models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )
    feedback = models.TextField(blank=True)
    rating = models.PositiveIntegerField(null=True, blank=True, help_text='1-10')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['scheduled_date']

    def __str__(self):
        return f"{self.application} - {self.get_interview_type_display()}"


class OfferLetter(models.Model):
    """Offer letters for selected students."""

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'
        EXPIRED = 'EXPIRED', 'Expired'

    application = models.OneToOneField(
        'jobs.Application',
        on_delete=models.CASCADE,
        related_name='offer_letter',
    )
    package_offered = models.CharField(max_length=100)
    joining_date = models.DateField(null=True, blank=True)
    offer_details = models.TextField()
    file = models.FileField(upload_to='offer_letters/', blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    issued_at = models.DateTimeField(auto_now_add=True)
    response_deadline = models.DateField(null=True, blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-issued_at']

    def __str__(self):
        return f"Offer - {self.application.student.enrollment_no}"
