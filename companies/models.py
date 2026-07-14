"""
Company and recruiter profile models.
"""
from django.conf import settings
from django.db import models


class CompanyProfile(models.Model):
    """Company/recruiter profile with verification status."""

    class CompanySize(models.TextChoices):
        STARTUP = 'STARTUP', 'Startup (1-50)'
        SMALL = 'SMALL', 'Small (51-200)'
        MEDIUM = 'MEDIUM', 'Medium (201-1000)'
        LARGE = 'LARGE', 'Large (1000+)'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='company_profile',
    )
    company_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    headquarters = models.CharField(max_length=200, blank=True)
    company_size = models.CharField(
        max_length=20,
        choices=CompanySize.choices,
        default=CompanySize.MEDIUM,
    )
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    contact_person = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['company_name']
        verbose_name_plural = 'Company profiles'

    def __str__(self):
        return self.company_name
